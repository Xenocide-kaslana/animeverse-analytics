import streamlit as st

from src.analytics import count_by_year, executive_kpis, generate_insights, score_tier_distribution
from src.charts import bar_chart, line_chart
from src.genre_analysis import top_genres
from src.ui_components import chart_container, insight_card, kpi_card, page_header, section_header


def render(df, theme):
    with st.container():
        page_header("Ringkasan Utama", "Tinjauan volume, rating, studio, dan skala audiens anime.")
    kpi = executive_kpis(df)
    cards = st.columns(4)
    with cards[0]:
        kpi_card("Jumlah Anime", f"{kpi['total_anime']:,}".replace(",", "."), "Data setelah difilter")
    with cards[1]:
        mal_score_text = "Tidak tersedia" if kpi["average_mal_score"] is None else f"{kpi['average_mal_score']:.2f}".replace(".", ",")
        kpi_card("Rata-rata Skor MAL", mal_score_text, "Data skor tersedia")
    with cards[2]:
        kpi_card("Jumlah Studio Valid", f"{kpi['total_valid_studios']:,}".replace(",", "."), "Unknown tidak disertakan")
    with cards[3]:
        members_text = "Tidak tersedia" if kpi["average_mal_members"] is None else f"{kpi['average_mal_members']:,.0f}".replace(",", ".")
        kpi_card("Rata-rata Anggota MAL", members_text, "Data tersedia")

    section_header("Ringkasan Industri")
    left, right = st.columns(2)
    type_df = __import__("src.analytics", fromlist=["count_by_type"]).count_by_type(df)
    with left:
        chart_container("Distribusi Jenis Anime", "Jumlah anime berdasarkan format setelah difilter")
        st.plotly_chart(bar_chart(type_df, "type", "anime_count", theme), width="stretch", key="exec_type_chart")
    with right:
        year_df = count_by_year(df)
        chart_container("Tren Rilis Anime", "Jumlah rilis berdasarkan tahun yang tersedia")
        st.plotly_chart(line_chart(year_df, "year", "anime_count", theme), width="stretch", key="exec_year_chart")

    left, right = st.columns(2)
    tiers = score_tier_distribution(df)
    with left:
        chart_container("Distribusi Kategori Skor MAL", "Distribusi kategori skor pada dataset")
        st.plotly_chart(bar_chart(tiers, "score_tier", "anime_count", theme), width="stretch", key="exec_tier_chart")
    with right:
        genres = top_genres(df, 10)
        chart_container("10 Genre Teratas", "Frekuensi genre pada anime yang difilter")
        st.plotly_chart(bar_chart(genres, "genre", "anime_count", theme, horizontal=True), width="stretch", key="exec_genre_chart")

    section_header("Insight Utama")
    for index, insight in enumerate(generate_insights(df)):
        insight_card(f"Insight {index + 1}", insight, "success" if index % 2 == 0 else "violet")
