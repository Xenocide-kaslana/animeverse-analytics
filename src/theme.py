from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from src.localization import t


COLORS = {
    "navy": "#171426",
    "secondary_dark": "#242039",
    "violet": "#C5ADED",
    "lavender": "#C5ADED",
    "light": "#FAF8FF",
    "white": "#FFFFFF",
    "text": "#21164D",
    "text_secondary": "#655D78",
    "border_light": "#DDD3EE",
    "grid_light": "#E5DDF0",
    "text_dark": "#F8F5FF",
    "text_secondary_dark": "#C3BAD8",
    "border_dark": "#39314E",
    "success": "#BCE0FF",
    "warning": "#F8ABEB",
    "pink": "#F8ABEB",
    "soft_pink": "#FFC8DD",
    "baby_blue": "#BCE0FF",
    "sky_blue": "#A2D2FF",
}


def initialize_theme() -> str:
    if "animeverse_theme" not in st.session_state:
        st.session_state["animeverse_theme"] = "Light"
    return st.session_state["animeverse_theme"]


def render_theme_switcher() -> str:
    theme = st.sidebar.radio(
        t("Appearance"),
        [t("Light"), t("Dark")],
        index=0 if st.session_state["animeverse_theme"] == "Light" else 1,
        horizontal=True,
        key="theme_switcher",
    )
    selected = "Light" if theme == t("Light") else "Dark"
    st.session_state["animeverse_theme"] = selected
    return selected


def apply_theme(theme: str) -> None:
    st.session_state["animeverse_theme"] = theme


def plotly_template(theme: str) -> dict:
    dark = theme == "Dark"
    text = "#F8F5FF" if dark else COLORS["text"]
    secondary = "#C3BAD8" if dark else "#655D78"
    grid = "#39314E" if dark else "#E5DDF0"
    card = "#242039" if dark else "#FFFFFF"
    background = COLORS["navy"] if dark else COLORS["light"]
    border = "#39314E" if dark else "#DDD3EE"
    hover_background = "#242039" if dark else "#FFFFFF"
    return {
        "paper_bgcolor": card,
        "plot_bgcolor": card,
        "font": {"family": "Inter, sans-serif", "size": 12, "color": text},
        "text_color": text,
        "secondary_text_color": secondary,
        "border_color": border,
        "hover_bgcolor": hover_background,
        "xaxis": {"gridcolor": grid, "zerolinecolor": grid, "tickcolor": secondary, "linecolor": border, "title_font_color": text, "tick_font_color": secondary},
        "yaxis": {"gridcolor": grid, "zerolinecolor": grid, "tickcolor": secondary, "linecolor": border, "title_font_color": text, "tick_font_color": secondary},
        "background": background,
    }
