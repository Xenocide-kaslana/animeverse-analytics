import streamlit as st

from src.charts import bar_chart, heatmap
from src.streaming_analysis import (
    anime_count_per_platform, anime_multiple_platforms, platform_average_score,
    platform_count_distribution, platform_vs_genre,
)
from src.ui_components import chart_container, data_table, page_header, section_header


def render(df, theme):
    with st.container():
        page_header("Analisis Platform Streaming", "Ketersediaan platform, skor, dan cakupan genre lintas platform. Data kosong tidak dianggap sebagai tidak tersedia.")
    section_header("Cakupan Platform")
    platform_count = anime_count_per_platform(df)
    left, right = st.columns(2)
    with left:
        chart_container("Jumlah Anime pada Setiap Platform Streaming", "True, false, dan unknown ditampilkan terpisah")
        st.plotly_chart(bar_chart(platform_count, "platform", "true_count", theme, horizontal=True), width="stretch", key="stream_true_chart")
        st.dataframe(platform_count, width="stretch", hide_index=True)
    with right:
        chart_container("Rata-rata Skor MAL per Platform", "Skor tersedia pada data dengan status True")
        st.plotly_chart(bar_chart(platform_average_score(df), "platform", "average_mal_score", theme, horizontal=True), width="stretch", key="stream_score_chart")

    section_header("Jangkauan Platform")
    left, right = st.columns(2)
    with left:
        chart_container("Distribusi Jumlah Platform", "Label unknown tetap dipisahkan")
        st.plotly_chart(bar_chart(platform_count_distribution(df), "platform_count", "anime_count", theme), width="stretch", key="stream_platform_count_chart")
    with right:
        chart_container("Platform vs Genre", "Frekuensi pada data dengan penanda platform positif")
        platform_genre = platform_vs_genre(df)
        st.plotly_chart(heatmap(platform_genre, "genre", "platform", "anime_count", theme), width="stretch", key="stream_genre_heatmap")

    section_header("Anime Multi-platform")
    multi = anime_multiple_platforms(df, 2)
    chart_container("Anime yang Tersedia pada Banyak Platform", f"{len(multi):,} data memiliki minimal dua platform aktif".replace(",", "."))
    data_table(multi, page_size=10, key_prefix="stream_multi_table", columns=[
        "title_english", "type", "year", "mal_score", "platform_count"
    ])
