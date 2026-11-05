import pandas as pd

from src.config import PLATFORM_COLUMNS


def platform_status(df: pd.DataFrame, column: str) -> pd.Series:
    availability = df[column].map({True: "True", False: "False"}) if pd.api.types.is_bool_dtype(df[column]) else pd.Series("Unknown", index=df.index)
    text_recorded = df["streaming_platforms"].notna()
    return availability.where(text_recorded, "Unknown")


def anime_count_per_platform(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, column in PLATFORM_COLUMNS.items():
        if column in df:
            recorded = df["streaming_platforms"].notna()
            rows.append({
                "platform": name,
                "true_count": int(df[column].fillna(False).astype(bool).sum()),
                "false_count": int((recorded & ~df[column].fillna(False).astype(bool)).sum()),
                "unknown_count": int(df["streaming_platforms"].isna().sum()),
            })
    return pd.DataFrame(rows)


def platform_average_score(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, column in PLATFORM_COLUMNS.items():
        if column in df:
            available = df.loc[df[column].fillna(False).astype(bool)]
            rows.append({"platform": name, "average_mal_score": available["mal_score"].mean(),
                         "sample_count": int(available["mal_score"].notna().sum())})
    return pd.DataFrame(rows).sort_values("average_mal_score", ascending=False)


def platform_count_distribution(df: pd.DataFrame) -> pd.DataFrame:
    columns = [column for column in PLATFORM_COLUMNS.values() if column in df]
    recorded = df["streaming_platforms"].notna()
    counts = df.loc[recorded, columns].fillna(False).astype(bool).sum(axis=1)
    distribution = counts.value_counts().rename_axis("platform_count").reset_index(name="anime_count")
    unknown = pd.DataFrame([{
        "platform_count": "Unknown/missing",
        "anime_count": int((~recorded).sum()),
    }])
    return pd.concat([distribution, unknown], ignore_index=True).sort_values("anime_count", ascending=False).reset_index(drop=True)


def platform_vs_genre(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    genre_rows = df.explode("genre_list").rename(columns={"genre_list": "genre"}).dropna(subset=["genre"])
    for name, column in PLATFORM_COLUMNS.items():
        if column in df:
            counts = genre_rows.loc[genre_rows[column].fillna(False).astype(bool), "genre"].value_counts()
            rows.extend({"platform": name, "genre": genre, "anime_count": int(count)}
                        for genre, count in counts.items())
    return pd.DataFrame(rows).sort_values(["platform", "anime_count"], ascending=[True, False])


def anime_multiple_platforms(df: pd.DataFrame, minimum: int = 2) -> pd.DataFrame:
    columns = [column for column in PLATFORM_COLUMNS.values() if column in df]
    counts = df[columns].fillna(False).astype(bool).sum(axis=1)
    result = df.loc[counts >= minimum].copy()
    result["platform_count"] = counts[counts >= minimum]
    return result
