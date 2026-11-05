import streamlit as st

from src.charts import bar_chart, heatmap
from src.genre_analysis import genre_average_score, genre_by_anime_type, genre_frequency
from src.studio_analysis import studio_vs_genre, top_studios_by_average_score, top_studios_by_count
from src.ui_components import chart_container, page_header, section_header


def render(df, theme):
    with st.container():
        page_header("Studio & Genre", "Mitra produksi dan komposisi genre dengan batas jumlah sampel.")
    section_header("Peringkat Studio")
    left, right = st.columns(2)
    with left:
        chart_container("10 Studio dengan Jumlah Produksi Terbanyak", "Unknown tidak disertakan")
        st.plotly_chart(bar_chart(top_studios_by_count(df, 10), "studio", "anime_count", theme, horizontal=True), width="stretch", key="studio_count_chart")
    with right:
        studio_scores = top_studios_by_average_score(df, 10, 5)
        chart_container("10 Studio dengan Rata-rata Skor MAL Terbaik", "Minimum 5 anime yang memiliki skor")
        st.plotly_chart(bar_chart(studio_scores, "studio", "average_mal_score", theme, horizontal=True), width="stretch", key="studio_score_chart")

    section_header("Analisis Genre")
    left, right = st.columns(2)
    with left:
        chart_container("Frekuensi Genre", "Genre teratas berdasarkan jumlah anime")
        st.plotly_chart(bar_chart(genre_frequency(df).head(15), "genre", "anime_count", theme, horizontal=True), width="stretch", key="genre_freq_chart")
    with right:
        chart_container("Rata-rata Skor Berdasarkan Genre", "Genre dengan minimal 30 anime")
        st.plotly_chart(bar_chart(genre_average_score(df, 30).head(15), "genre", "average_mal_score", theme, horizontal=True), width="stretch", key="genre_score_chart")

    left, right = st.columns(2)
    studio_genre = studio_vs_genre(df)
    with left:
        chart_container("Hubungan Studio dan Genre", "Studio teratas berdasarkan jumlah genre")
        top_studios = top_studios_by_count(df, 12)["studio"].tolist()
        subset = studio_genre[studio_genre["studio"].isin(top_studios)]
        st.plotly_chart(heatmap(subset, "genre", "studio", "anime_count", theme), width="stretch", key="studio_genre_heatmap")
    with right:
        chart_container("Distribusi Genre Berdasarkan Jenis Anime", "Jumlah genre menurut format")
        genre_type = genre_by_anime_type(df)
        pivot = genre_type.pivot(index="genre", columns="type", values="anime_count").fillna(0)
        top_genres = pivot.sum(axis=1).nlargest(15).index
        distribution = pivot.loc[top_genres].reset_index().melt(
            id_vars="genre",
            var_name="type",
            value_name="anime_count",
        )
        st.plotly_chart(
            heatmap(distribution, "genre", "type", "anime_count", theme),
            width="stretch",
            key="genre_type_heatmap",
        )
