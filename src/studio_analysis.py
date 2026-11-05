import pandas as pd

from src.config import MIN_STUDIO_ANIME


def _valid_studio_rows(df: pd.DataFrame) -> pd.DataFrame:
    studios = df["studio_main"].fillna("")
    return df.loc[studios.str.strip().ne("") & studios.str.lower().ne("unknown")].copy()


def top_studios_by_count(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    return (
        _valid_studio_rows(df)["studio_main"].value_counts()
        .head(n).rename_axis("studio").reset_index(name="anime_count")
    )


def studio_average_score(df: pd.DataFrame, min_anime: int = MIN_STUDIO_ANIME) -> pd.DataFrame:
    studios = _valid_studio_rows(df).dropna(subset=["mal_score"])
    result = (
        studios.groupby("studio_main", as_index=False)
        .agg(anime_count=("mal_id", "nunique"), average_mal_score=("mal_score", "mean"))
        .query("anime_count >= @min_anime")
        .sort_values(["average_mal_score", "anime_count"], ascending=[False, False])
    )
    return result.rename(columns={"studio_main": "studio"}).reset_index(drop=True)


def top_studios_by_average_score(
    df: pd.DataFrame, n: int = 20, min_anime: int = MIN_STUDIO_ANIME
) -> pd.DataFrame:
    return studio_average_score(df, min_anime).head(n)


def studio_vs_genre(df: pd.DataFrame) -> pd.DataFrame:
    studios = _valid_studio_rows(df).explode("genre_list").rename(columns={"genre_list": "genre"})
    studios = studios.dropna(subset=["genre"])
    return (
        studios.groupby(["studio_main", "genre"], observed=True)["mal_id"].nunique()
        .rename("anime_count").reset_index()
        .rename(columns={"studio_main": "studio"})
    )


def studio_distribution_by_type(df: pd.DataFrame) -> pd.DataFrame:
    studios = _valid_studio_rows(df)
    return (
        studios.groupby(["studio_main", "type"], observed=True)["mal_id"].nunique()
        .rename("anime_count").reset_index()
        .rename(columns={"studio_main": "studio"})
    )
