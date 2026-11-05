import pandas as pd

from src.config import MIN_GENRE_ANIME


def explode_genres(df: pd.DataFrame) -> pd.DataFrame:
    if "genre_list" not in df:
        raise ValueError("Dataset does not contain genre_list.")
    return df[["mal_id", "title_english", "type", "mal_score", "mal_members", "genre_list"]].explode(
        "genre_list"
    ).rename(columns={"genre_list": "genre"}).dropna(subset=["genre"])


def genre_frequency(df: pd.DataFrame) -> pd.DataFrame:
    return (
        explode_genres(df)["genre"].value_counts()
        .rename_axis("genre").reset_index(name="anime_count")
    )


def top_genres(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return genre_frequency(df).head(n)


def genre_average_score(df: pd.DataFrame, min_anime: int = MIN_GENRE_ANIME) -> pd.DataFrame:
    genre_rows = explode_genres(df).dropna(subset=["mal_score"])
    result = (
        genre_rows.groupby("genre", as_index=False)
        .agg(anime_count=("mal_id", "nunique"), average_mal_score=("mal_score", "mean"))
        .query("anime_count >= @min_anime")
        .sort_values(["average_mal_score", "anime_count"], ascending=[False, False])
    )
    return result.reset_index(drop=True)


def genre_score_distribution(df: pd.DataFrame, genre: str) -> pd.DataFrame:
    rows = explode_genres(df)
    return rows.loc[rows["genre"].eq(genre), ["mal_id", "title_english", "mal_score"]].dropna(subset=["mal_score"])


def genre_by_anime_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        explode_genres(df).dropna(subset=["type"])
        .groupby(["genre", "type"], observed=True)["mal_id"].nunique()
        .rename("anime_count").reset_index()
        .sort_values(["genre", "anime_count"], ascending=[True, False])
    )


def genre_correlation(df: pd.DataFrame, genres: list[str] | None = None) -> pd.DataFrame:
    rows = explode_genres(df)
    if genres is None:
        genres = genre_frequency(df).head(20)["genre"].tolist()
    matrix = pd.crosstab(rows["mal_id"], rows["genre"]).reindex(columns=genres, fill_value=0)
    if matrix.shape[1] < 2:
        return pd.DataFrame(columns=["genre_1", "genre_2", "correlation"])
    corr = matrix.corr(numeric_only=True).stack().reset_index()
    corr.columns = ["genre_1", "genre_2", "correlation"]
    corr = corr[corr["genre_1"] < corr["genre_2"]]
    return corr.dropna().sort_values("correlation", ascending=False).reset_index(drop=True)
