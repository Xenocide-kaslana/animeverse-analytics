from pathlib import Path
import json

import pandas as pd


RAW_DATA = Path(__file__).resolve().parents[1] / "data" / "raw" / "anime_dataset_20k.csv"
REPORT = Path(__file__).resolve().parents[1] / "data" / "inspection_report.json"


def summarize() -> dict:
    df = pd.read_csv(RAW_DATA)
    missing = df.isna().sum()
    platform_columns = [
        column for column in df.columns
        if column.startswith("is_") and column not in {"is_adult", "is_long_running", "is_movie"}
    ]

    invalid_mal_scores = df["mal_score"].notna() & ~df["mal_score"].between(0, 10)
    invalid_anilist_scores = df["anilist_score"].notna() & ~df["anilist_score"].between(0, 10)
    invalid_episodes = df["episodes"].notna() & (df["episodes"] < 0)

    return {
        "source": str(RAW_DATA),
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "columns": df.columns.tolist(),
        "mal_id_duplicates": int(df["mal_id"].duplicated().sum()),
        "missing_values": {
            column: int(count) for column, count in missing.items() if count > 0
        },
        "missing_percent": {
            column: round(float(count / len(df) * 100), 2)
            for column, count in missing.items() if count > 0
        },
        "year_range": {
            "min": None if df["year"].isna().all() else int(df["year"].min()),
            "max": None if df["year"].isna().all() else int(df["year"].max()),
        },
        "type_counts": {
            str(key): int(value)
            for key, value in df["type"].value_counts(dropna=False).items()
        },
        "season_counts": {
            ("Unknown" if pd.isna(key) else str(key)): int(value)
            for key, value in df["season"].value_counts(dropna=False).items()
        },
        "studio_unknown_rows": int(df["studio_main"].fillna("").str.strip().eq("").sum()
                                   + df["studio_main"].fillna("").str.strip().str.lower().eq("unknown").sum()),
        "missing_genres": int(df["genres"].isna().sum()),
        "platform_columns": platform_columns,
        "platform_counts": {
            column: int(pd.to_numeric(df[column], errors="coerce").fillna(False).astype(bool).sum())
            for column in platform_columns
        },
        "rating_validation": {
            "mal_range": [float(df["mal_score"].min()), float(df["mal_score"].max())],
            "anilist_range": [float(df["anilist_score"].min()), float(df["anilist_score"].max())],
            "invalid_mal_scores": int(invalid_mal_scores.sum()),
            "invalid_anilist_scores": int(invalid_anilist_scores.sum()),
            "invalid_negative_episodes": int(invalid_episodes.sum()),
            "zero_episode_rows": int((df["episodes"] == 0).sum()),
        },
        "duplicate_platform_and_streaming_rows": int(
            df.duplicated(subset=platform_columns + ["streaming_platforms"]).sum()
        ),
    }


if __name__ == "__main__":
    report = summarize()
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
