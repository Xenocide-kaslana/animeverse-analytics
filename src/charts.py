import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.localization import AXIS_LABELS

from src.theme import COLORS, plotly_template


def themed_layout(fig: go.Figure, theme: str, title: str | None = None, height: int = 360):
    template = plotly_template(theme)
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=55, r=25, t=55 if title else 25, b=55),
        paper_bgcolor=template["paper_bgcolor"],
        plot_bgcolor=template["plot_bgcolor"],
        font=template["font"],
        title_font=dict(family="Inter, sans-serif", size=16, color=template["text_color"]),
        colorway=[
            COLORS["lavender"],
            COLORS["pink"],
            COLORS["soft_pink"],
            COLORS["baby_blue"],
            COLORS["sky_blue"],
        ],
    )
    axis_defaults = dict(
        gridcolor=template["xaxis"]["gridcolor"],
        zerolinecolor=template["xaxis"]["zerolinecolor"],
        tickcolor=template["xaxis"]["tickcolor"],
        linecolor=template["border_color"],
        tickfont=dict(family="Inter, sans-serif", size=11, color=template["xaxis"]["tick_font_color"]),
        title_font=dict(family="Inter, sans-serif", size=12, color=template["xaxis"]["title_font_color"]),
    )
    fig.update_xaxes(**axis_defaults)
    fig.update_yaxes(**axis_defaults)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=template["hover_bgcolor"],
            bordercolor=template["border_color"],
            font=dict(family="Inter, sans-serif", size=12, color=template["text_color"]),
        ),
        legend=dict(font=dict(family="Inter, sans-serif", size=12, color=template["text_color"])),
    )
    x_title = fig.layout.xaxis.title.text if fig.layout.xaxis.title else None
    y_title = fig.layout.yaxis.title.text if fig.layout.yaxis.title else None
    fig.update_xaxes(title_text=AXIS_LABELS.get(x_title, x_title))
    fig.update_yaxes(title_text=AXIS_LABELS.get(y_title, y_title))
    fig.update_traces(
        hovertemplate="%{x}<br>%{y}<extra></extra>"
    )
    return fig


def localize_axes(fig: go.Figure) -> go.Figure:
    fig.update_xaxes(title_text=AXIS_LABELS.get(fig.layout.xaxis.title.text or "", fig.layout.xaxis.title.text or None))
    fig.update_yaxes(title_text=AXIS_LABELS.get(fig.layout.yaxis.title.text or "", fig.layout.yaxis.title.text or None))
    return fig


def bar_chart(data: pd.DataFrame, x: str, y: str, theme: str, title: str = "", horizontal: bool = False, height: int = 360):
    if data.empty:
        return themed_layout(go.Figure(), theme, title, height)
    if horizontal:
        fig = px.bar(data, x=y, y=x, orientation="h", color_discrete_sequence=[COLORS["violet"]])
        fig.update_yaxes(categoryorder="total ascending")
    else:
        fig = px.bar(data, x=x, y=y, color_discrete_sequence=[COLORS["violet"]])
    return themed_layout(fig, theme, title, height)


def line_chart(data: pd.DataFrame, x: str, y: str, theme: str, title: str = ""):
    if data.empty:
        return themed_layout(go.Figure(), theme, title)
    fig = px.line(data, x=x, y=y, markers=True, color_discrete_sequence=[COLORS["violet"]])
    fig.update_traces(line_width=3)
    return themed_layout(fig, theme, title)


def histogram(data: pd.DataFrame, column: str, theme: str, title: str = "", nbins: int = 40):
    if data.empty or column not in data.columns:
        return themed_layout(go.Figure(), theme, title)
    values = pd.to_numeric(data[column], errors="coerce").dropna()
    if values.empty:
        return themed_layout(go.Figure(), theme, title)
    plot_data = pd.DataFrame({column: values.to_numpy(dtype=float)})
    fig = px.histogram(plot_data, x=column, nbins=nbins, color_discrete_sequence=[COLORS["violet"]])
    return themed_layout(fig, theme, title)


def scatter(data: pd.DataFrame, x: str, y: str, theme: str, title: str = "", hover_name: str | None = None):
    required_columns = [x, y] + ([hover_name] if hover_name else [])
    if data.empty or any(column not in data.columns for column in required_columns):
        return themed_layout(go.Figure(), theme, title, 420)
    sample = data[required_columns].copy()
    sample[x] = pd.to_numeric(sample[x], errors="coerce")
    sample[y] = pd.to_numeric(sample[y], errors="coerce")
    sample = sample.dropna()
    if sample.empty:
        return themed_layout(go.Figure(), theme, title, 420)
    fig = px.scatter(
        sample, x=x, y=y, hover_name=hover_name, color_discrete_sequence=[COLORS["lavender"]],
        opacity=0.65,
    )
    fig.update_traces(marker_size=7)
    return themed_layout(fig, theme, title, 420)


def heatmap(data: pd.DataFrame, x: str, y: str, value: str, theme: str, title: str = ""):
    if data.empty:
        return themed_layout(go.Figure(), theme, title, 520)
    matrix = data.pivot(index=y, columns=x, values=value).fillna(0)
    fig = go.Figure(go.Heatmap(
        z=matrix.values, x=matrix.columns, y=matrix.index,
        colorscale=[[0, "#F5F3FF"], [0.5, "#A78BFA"], [1, "#4C1D95"]],
        colorbar=dict(title=value),
    ))
    return themed_layout(fig, theme, title, 520)
