import streamlit as st

from src.analytics import count_by_decade, count_by_source, count_by_type, count_by_year, count_by_season, episode_distribution
from src.charts import bar_chart, line_chart
from src.ui_components import chart_container, page_header, section_header


def render(df, theme):
    with st.container():
        page_header("Tren Anime", "Pola rilis, format, sumber cerita, musim tayang, dan jumlah episode.")
    section_header("Aktivitas Rilis")
    left, right = st.columns(2)
    with left:
        chart_container("Tren Rilis Berdasarkan Tahun", "Tahun yang tidak tersedia tidak disertakan")
        st.plotly_chart(line_chart(count_by_year(df), "year", "anime_count", theme), width="stretch", key="trends_year_chart")
    with right:
        chart_container("Distribusi Rilis Berdasarkan Dekade", "Dihitung hanya dari tahun rilis yang tersedia")
        st.plotly_chart(bar_chart(count_by_decade(df), "decade", "anime_count", theme), width="stretch", key="trends_decade_chart")

    section_header("Format dan Produksi")
    left, right = st.columns(2)
    with left:
        chart_container("Anime Berdasarkan Musim", "Label musim yang tersedia")
        st.plotly_chart(bar_chart(count_by_season(df), "season", "anime_count", theme), width="stretch", key="trends_season_chart")
    with right:
        chart_container("Distribusi Jenis Anime", "Distribusi berdasarkan format")
        st.plotly_chart(bar_chart(count_by_type(df), "type", "anime_count", theme, horizontal=True), width="stretch", key="trends_type_chart")

    left, right = st.columns(2)
    with left:
        chart_container("Distribusi Materi Sumber", "Distribusi berdasarkan sumber cerita")
        st.plotly_chart(bar_chart(count_by_source(df).head(15), "source", "anime_count", theme, horizontal=True), width="stretch", key="trends_source_chart")
    with right:
        episodes = episode_distribution(df)
        chart_container("Distribusi Episode", "Jumlah episode positif; nilai nol dan kosong tidak disertakan")
        st.plotly_chart(line_chart(episodes.head(300), "episodes", "anime_count", theme), width="stretch", key="trends_episode_chart")
