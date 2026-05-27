# =============================================================================
# app.py — TERIIP Multicentre Blood Parameter Analytics Dashboard
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from config import STANDARD_PARAMS, PARAM_GROUPS, CENTRE_METADATA, AGE_LABELS
from data_loader import load_master, get_centre_summary, get_param_availability

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TERIIP Analytics Dashboard",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- Base ---------- */
    [data-testid="stAppViewContainer"] { background: #0f1117; }
    [data-testid="stSidebar"]          { background: #161b27; border-right: 1px solid #2a3045; }
    h1, h2, h3, h4                     { color: #e8ecf4 !important; font-family: 'Segoe UI', sans-serif; }
    p, li, label, span                 { color: #b0bcd0 !important; }

    /* ---------- KPI cards ---------- */
    .kpi-row { display: flex; gap: 14px; margin-bottom: 8px; flex-wrap: wrap; }
    .kpi-card {
        flex: 1; min-width: 150px;
        background: linear-gradient(135deg, #1a2035 0%, #1e2845 100%);
        border: 1px solid #2e3f5c;
        border-radius: 12px;
        padding: 18px 20px 14px;
        text-align: center;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #5b9cf6 !important; line-height: 1.1; }
    .kpi-label { font-size: 0.75rem; color: #7a8eab !important; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.06em; }

    /* ---------- Section headers ---------- */
    .section-header {
        font-size: 1rem; font-weight: 600; color: #5b9cf6 !important;
        text-transform: uppercase; letter-spacing: 0.08em;
        border-left: 3px solid #5b9cf6; padding-left: 10px;
        margin: 28px 0 14px;
    }

    /* ---------- Divider ---------- */
    hr { border: none; border-top: 1px solid #2a3045; margin: 20px 0; }

    /* ---------- Plotly chart bg ---------- */
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }

    /* ---------- Sidebar label style ---------- */
    [data-testid="stSidebar"] label { color: #8ca3c0 !important; font-size: 0.82rem; }

    /* ---------- Expander ---------- */
    [data-testid="stExpander"] { background: #13192a; border: 1px solid #2a3045; border-radius: 8px; }

    /* ---------- Table ---------- */
    [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#b0bcd0",
    font_family="Segoe UI, sans-serif",
)
GRID_STYLE = dict(gridcolor="#1f2d40", zerolinecolor="#2a3a50")


# =============================================================================
# HELPERS
# =============================================================================

def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"], family=CHART_THEME["font_family"]),
        margin=dict(t=40, b=30, l=10, r=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#b0bcd0"),
    )
    fig.update_xaxes(**GRID_STYLE)
    fig.update_yaxes(**GRID_STYLE)
    return fig


def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)


def kpi_cards(items: list[tuple]):
    """items = [(value, label), ...]"""
    cards_html = '<div class="kpi-row">'
    for val, label in items:
        cards_html += (
            f'<div class="kpi-card">'
            f'<div class="kpi-value">{val}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'</div>'
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


# =============================================================================
# DATA LOAD
# =============================================================================

master_full = load_master()
centre_summary_full = get_centre_summary(master_full)

# =============================================================================
# SIDEBAR — FILTERS
# =============================================================================

with st.sidebar:
    st.markdown("### 🔬 TERIIP Dashboard")
    st.markdown("*ICMR Multicentre Analytics*")
    st.markdown("---")

    all_regions = sorted(centre_summary_full["Region"].dropna().unique().tolist())
    sel_regions = st.multiselect(
        "Filter by Region",
        options=all_regions,
        default=all_regions,
        key="regions",
    )

    # Include ALL centres from metadata (even those with no data yet)
    centres_in_region = sorted(
        centre_summary_full[centre_summary_full["Region"].isin(sel_regions)]["Centre"]
        .dropna().unique().tolist()
    )
    sel_centres = st.multiselect(
        "Filter by Centre",
        options=centres_in_region,
        default=centres_in_region,
        key="centres",
    )

    st.markdown("---")
    st.markdown(
        f"<span style='font-size:0.72rem;color:#4a6080'>Last updated: "
        f"{datetime.now().strftime('%d %b %Y, %H:%M')}</span>",
        unsafe_allow_html=True,
    )

# ── Apply filters ─────────────────────────────────────────────────────────────
master = master_full[
    master_full["Region"].isin(sel_regions)
    & master_full["Display_Name"].isin(sel_centres)
].copy()

centre_summary = centre_summary_full[
    centre_summary_full["Region"].isin(sel_regions)
    & centre_summary_full["Centre"].isin(sel_centres)
].copy()

# =============================================================================
# HEADER
# =============================================================================

st.markdown(
    """
    <div style="padding: 8px 0 4px; text-align: center;">
        <h1 style="margin:0; font-size:1.7rem; color:#e8ecf4">
            🩸 TERIIP Multicentre Blood Parameter Analytics Dashboard
        </h1>
        <p style="margin:4px 0 0; font-size:0.88rem; color:#5b7ea6">
            Indian Council of Medical Research (ICMR)
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# =============================================================================
# SECTION 1 — KPI CARDS
# =============================================================================

section("📊 Project Overview")

total_centres    = centre_summary["Centre"].nunique()
params_tested    = sum(master[p].notna().any() for p in STANDARD_PARAMS)
samples          = 1100   # ← CHANGE THIS to your actual collected sample count: (len(master))
PARTICIPANTS_SCREENED = 6330   # ← CHANGE THIS to your actual screened count

kpi_cards([
    (total_centres,                                "Centres Active"),
    (f"{params_tested} / {len(STANDARD_PARAMS)}", "Parameters Available"),
    (f"{samples:,}",                               "Samples Collected"),
    (f"{PARTICIPANTS_SCREENED:,}",                     "Participants Screened"),
])

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# SECTION 2 — INDIA MAP
# =============================================================================

section("🗺️ Centre Locations — India")

map_df = centre_summary.copy()
map_df["bubble_size"] = map_df["Achieved"].clip(lower=5)

fig_map = go.Figure()

# Colour scale based on completion %
colorscale = [[0, "#c0392b"], [0.5, "#e67e22"], [1.0, "#27ae60"]]

fig_map.add_trace(
    go.Scattergeo(
        lat=map_df["lat"],
        lon=map_df["lon"],
        mode="markers+text",
        marker=dict(
            size=map_df["bubble_size"] / 4,
            sizemode="area",
            sizeref=1,
            color=map_df["Completion_%"],
            colorscale=colorscale,
            cmin=0, cmax=100,
            colorbar=dict(
                title=dict(text="Completion %", font=dict(color="#b0bcd0")),
                tickfont=dict(color="#b0bcd0"),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="#2a3045",
            ),
            line=dict(color="#2a3a55", width=1),
        ),
        text=map_df["Centre"],
        textposition="top center",
        textfont=dict(size=9, color="#b0bcd0"),
        customdata=np.stack(
            [map_df["Region"], map_df["NABL_Biochem"], map_df["NABL_Haem"], map_df["DOS"],
             map_df["Target"], map_df["Achieved"], map_df["Completion_%"]], axis=-1
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Region: %{customdata[0]}<br>"
            "NABL: %{customdata[1]}<br>"
            "DOS: %{customdata[2]}<br>"
            "Target: %{customdata[3]}<br>"
            "Achieved: %{customdata[4]}<br>"
            "Completion: %{customdata[5]}%"
            "<extra></extra>"
        ),
    )
)

fig_map.update_layout(
    geo=dict(
        scope="asia",
        resolution=50,
        showland=True, landcolor="#1a2035",
        showocean=True, oceancolor="#0f1420",
        showcountries=True, countrycolor="#2a3a55",
        showlakes=False,
        lataxis_range=[6, 38],
        lonaxis_range=[66, 98],
        bgcolor="rgba(0,0,0,0)",
        framecolor="#2a3045",
    ),
    height=480,
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#b0bcd0",
    margin=dict(t=10, b=0, l=0, r=0),
)

st.plotly_chart(fig_map, use_container_width=True)

# =============================================================================
# SECTION 3 — CENTRE PERFORMANCE TABLE
# =============================================================================

section("🏥 Centre-wise Performance")

def colour_completion(val):
    try:
        v = float(val)
        if v >= 80:
            return "background-color: #1a3a2a; color: #4ade80"
        elif v >= 50:
            return "background-color: #2a2d1a; color: #facc15"
        else:
            return "background-color: #3a1a1a; color: #f87171"
    except Exception:
        return ""

display_cols = ["Centre", "Region", "NABL_Biochem", "NABL_Haem", "DOS", "Target", "Achieved", "Completion_%"]
table_df = centre_summary[display_cols].reset_index(drop=True)
table_df.index = table_df.index + 1  # start from 1
styled = (
    table_df
    .style
    .map(colour_completion, subset=["Completion_%"])
    .format({"Completion_%": "{:.1f}%"})
    .set_properties(**{"background-color": "#111827", "color": "#c8d4e4", "border": "1px solid #1f2d40"})
    .set_table_styles(
        [{"selector": "thead th", "props": [("background-color", "#1a2540"), ("color", "#7ab4f5"), ("font-size", "0.78rem")]}]
    )
)
st.dataframe(styled, use_container_width=True, height=400)

# =============================================================================
# SECTION 4 — RECRUITMENT FUNNEL
# =============================================================================

section("🔽 Recruitment Funnel")

# ── Update these four numbers with your actual values ──────────────────────
FUNNEL_SCREENED  = 6330   # total participants screened
FUNNEL_ELIGIBLE  = 1894   # eligible after screening
FUNNEL_COLLECTED = 1100   # samples actually collected

fig_funnel = go.Figure(
    go.Funnel(
        y=["Participants Screened", "Eligible", "Samples Collected"],
        x=[FUNNEL_SCREENED, FUNNEL_ELIGIBLE, FUNNEL_COLLECTED],
        textinfo="value+percent initial",
        marker=dict(color=["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7"]),
        connector=dict(line=dict(color="#2a3a55", width=2)),
    )
)
fig_funnel.update_layout(height=320, **CHART_THEME, margin=dict(t=20, b=10, l=60, r=10))
st.plotly_chart(fig_funnel, use_container_width=True)

# ── Drilldown: centre-wise breakdown ─────────────────────────────────────
drill_stage = st.selectbox(
        "Drill down — select a stage to see centre-wise numbers:",
        options=["Patients Screened", "Eligible", "Samples Collected"],
        key="funnel_drill",
    )

    # Fill in your actual centre-wise numbers here.
    # Keys must match the Centre_Key column in centre_summary.
CENTRE_FUNNEL_DATA = {
        # "Centre_Key":  [Screened, Eligible, Collected]
        "AIIMS_Jodhpur":       [220, 200, 185],
        "AIIMS_Bhatinda":      [210, 195, 180],
        "AIIMS_Bhopal":        [200, 185, 170],
        "AIIMS_Raipur":        [190, 175, 160],
        "Amrita_Kochi":        [215, 200, 190],
        "Gleneagles_Chennai":  [180, 165, 150],
        "JSS_Mysore":          [205, 190, 178],
        "KIMS_Bhubaneswar":    [200, 185, 172],
        "KMC_Manipal":         [210, 195, 183],
        "PD_Hinduja_Mumbai":   [220, 205, 192],
        "AIIMS_Delhi":         [0, 0, 0],
        "AIIMS_Kalyani":       [0, 0, 0],
        "AIIMS_Guwahati":      [0, 0, 0],
        "DrBBCI_Guwahati":     [0, 0, 0],
        "KGMU_Lucknow":        [0, 0, 0],
        "PGIMER_Chandigarh":   [0, 0, 0],
    }

stage_idx = {"Patients Screened": 0, "Eligible": 1, "Samples Collected": 2}
idx = stage_idx[drill_stage]

drill_rows = []
for ck, vals in CENTRE_FUNNEL_DATA.items():
        display = CENTRE_METADATA.get(ck, {}).get("display_name", ck)
        drill_rows.append({"Centre": display, "Count": vals[idx]})
drill_df = pd.DataFrame(drill_rows).sort_values("Count", ascending=False)

fig_drill = px.bar(
        drill_df, x="Centre", y="Count",
        title=f"Centre-wise — {drill_stage}",
        color="Count",
        color_continuous_scale=[[0, "#1e3a5f"], [1, "#5b9cf6"]],
        text="Count",
    )
fig_drill.update_traces(textposition="outside", textfont_size=10)
fig_drill.update_coloraxes(showscale=False)
apply_chart_theme(fig_drill)
fig_drill.update_layout(
        height=350,
        xaxis_tickangle=-35,
        margin=dict(t=40, b=100, l=40, r=10),
    )
st.plotly_chart(fig_drill, use_container_width=True)

# =============================================================================
# SECTION 5 — DEMOGRAPHICS
# =============================================================================

section("👥 Patient Demographics")

col1, col2, col3 = st.columns(3)

# ── Age distribution ──────────────────────────────────────────────────────────
with col1:
    age_counts = master["Age_Group"].value_counts().reindex(AGE_LABELS, fill_value=0).reset_index()
    age_counts.columns = ["Age Group", "Participants Count"]
    fig_age = px.bar(
        age_counts, x="Age Group", y="Participants Count",
        color="Participants Count",
        color_continuous_scale=[[0, "#1e3a5f"], [1, "#5b9cf6"]],
        title="Age Distribution",
    )
    fig_age.update_coloraxes(showscale=False)
    apply_chart_theme(fig_age)
    fig_age.update_layout(height=300)
    st.plotly_chart(fig_age, use_container_width=True)

# ── Gender donut ──────────────────────────────────────────────────────────────
with col2:
    # Normalise gender values: M→Male, F→Female, everything else→Other
    gender_map = master["Gender"].str.strip().str.title()
    gender_map = gender_map.replace({
        "M": "Male", "F": "Female",
        "Transgender": "Other", "Trans": "Other",
        "Unknown": "Other", "Nan": "Other", "": "Other",
    })
    gender_map = gender_map.apply(lambda x: x if x in ["Male", "Female"] else "Other")
    gender_counts = gender_map.value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_gender = px.pie(
        gender_counts, names="Gender", values="Count",
        hole=0.6, title="Gender Ratio",
        color_discrete_map={"Male": "#5b9cf6", "Female": "#f472b6", "Other": "#94a3b8"},
    )
    fig_gender.update_traces(textposition="outside", textinfo="percent+label")
    apply_chart_theme(fig_gender)
    fig_gender.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_gender, use_container_width=True)
    
with col3:
    # ── Update these two numbers with your actual values ─────────────────
    RURAL_PCT  = 41.9   # percentage of rural participants
    URBAN_PCT  = 58.1   # percentage of urban participants
    # ─────────────────────────────────────────────────────────────────────
    ru_df = pd.DataFrame({
        "Category": ["Rural", "Urban"],
        "Percentage": [RURAL_PCT, URBAN_PCT],
    })
    fig_ru = px.pie(
        ru_df, names="Category", values="Percentage",
        hole=0.6, title="Rural vs Urban",
        color_discrete_map={"Rural": "#34d399", "Urban": "#818cf8"},
    )
    fig_ru.update_traces(textposition="outside", textinfo="percent+label")
    apply_chart_theme(fig_ru)
    fig_ru.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_ru, use_container_width=True)

# =============================================================================
# SECTION 6 — PARAMETER GROUP ANALYTICS
# =============================================================================

section("🧪 Parameter Group Analytics")

sel_group = st.selectbox(
    "Select Parameter Group",
    options=list(PARAM_GROUPS.keys()),
    key="param_group",
)

group_params = [p for p in PARAM_GROUPS[sel_group] if p in STANDARD_PARAMS]
group_df     = master[["Centre", "Display_Name", "Region", "Gender"] + group_params].copy()
SKIP_NUMERIC = ["Blood_Group", "PBS"]
available_params = [p for p in group_params if group_df[p].notna().any() and p not in SKIP_NUMERIC]

if not available_params:
    st.info("No data available for this parameter group under current filters.")
else:

    # ── 6a: Summary Statistics (first) ───────────────────────────────────────
    with st.expander("📊 Summary Statistics", expanded=True):
        desc   = master[available_params].describe().T
        skew   = master[available_params].skew().rename("skewness")
        stats  = pd.concat([desc, skew], axis=1).reset_index().rename(columns={"index": "Parameter"})
        col_order = ["Parameter", "count", "mean", "std", "min", "25%", "50%", "75%", "max", "skewness"]
        stats = stats[[c for c in col_order if c in stats.columns]].round(3)

        def _skew_label(val):
            try:
                v = float(val)
                if abs(v) < 0.5:
                    return "Symmetric"
                elif v >= 0.5 and v < 1.0:
                    return "Mildly Right-skewed"
                elif v >= 1.0:
                    return "Right-skewed"
                elif v <= -0.5 and v > -1.0:
                    return "Mildly Left-skewed"
                else:
                    return "Left-skewed"
            except Exception:
                return ""

        stats["skew_label"] = stats["skewness"].apply(_skew_label)

        def _colour_skew(val):
            try:
                v = float(val)
                if abs(v) < 0.5:
                    return "color: #4ade80"   # near-symmetric — green
                elif abs(v) < 1.0:
                    return "color: #facc15"   # moderate skew — yellow
                else:
                    return "color: #f87171"   # high skew — red
            except Exception:
                return ""

        st.dataframe(
            stats.style
            .map(_colour_skew, subset=["skewness"])
            .set_properties(subset=["skew_label"], **{"color": "#94a3b8", "font-style": "italic"})
            .format({c: "{:.3f}" for c in stats.columns if c not in ["Parameter", "count", "skew_label"]})
            .format({"count": "{:.0f}"})
            .set_properties(**{"background-color": "#111827", "color": "#c8d4e4",
                                "border": "1px solid #1f2d40"})
            .set_table_styles([{
                "selector": "thead th",
                "props": [("background-color", "#1a2540"), ("color", "#7ab4f5"), ("font-size", "0.78rem")]
            }]),
            use_container_width=True,
            height=min(500, 50 + 38 * len(stats)),
        )
        st.caption(
            "Skewness colour: green = symmetric (|s|<0.5), yellow = moderate (0.5–1.0), red = high (>1.0). "
            "Right-skewed = long right tail (high-value outliers). Left-skewed = long left tail (low-value outliers)."
        )

    # ── 6b: Value Distributions (histograms with KDE overlay) ────────────────
    with st.expander("📈 Value Distributions — All Centres Combined", expanded=True):
        st.caption(
            "Each histogram shows the distribution of measured values pooled across all centres "
            "currently selected. X-axis = lab value, Y-axis = patient count. "
            "The curve (KDE) shows the smoothed shape of the distribution."
        )
        n_cols = 3
        chunks = [available_params[i:i+n_cols] for i in range(0, len(available_params), n_cols)]
        for chunk in chunks:
            cols = st.columns(n_cols)
            for col_idx, param in enumerate(chunk):
                vals = master[param].dropna()
                if len(vals) == 0:
                    continue

                skew_val = float(vals.skew())
                skew_label = (
                    f"skew = {skew_val:+.2f} "
                    f"({'symmetric' if abs(skew_val) < 0.5 else 'right-skewed' if skew_val > 0 else 'left-skewed'})"
                )

                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(
                    x=vals, nbinsx=30,
                    histnorm="probability density",
                    marker_color="#3b82f6",
                    marker_line_color="#1e3a5f",
                    marker_line_width=0.5,
                    name="Distribution",
                    showlegend=False,
                ))

                # KDE overlay using numpy
                try:
                    from scipy.stats import gaussian_kde
                    kde_x = np.linspace(vals.min(), vals.max(), 200)
                    kde_y = gaussian_kde(vals)(kde_x)
                    fig_dist.add_trace(go.Scatter(
                        x=kde_x, y=kde_y,
                        mode="lines",
                        line=dict(color="#f97316", width=1.5),
                        name="KDE",
                        showlegend=False,
                    ))
                except Exception:
                    pass  # scipy not available — skip KDE silently

                fig_dist.update_layout(
                    title=dict(
                        text=f"{param.replace('_', ' ')}<br><sup style='color:#7a8eab'>{skew_label}</sup>",
                        font_size=11,
                    ),
                    height=220,
                    showlegend=False,
                    **CHART_THEME,
                    margin=dict(t=50, b=25, l=35, r=10),
                    xaxis=dict(tickfont_size=9, **GRID_STYLE),
                    yaxis=dict(tickfont_size=9, title="Density", **GRID_STYLE),
                )
                cols[col_idx].plotly_chart(fig_dist, use_container_width=True)

    # ── 6c: Regional Box Plots ────────────────────────────────────────────────
    with st.expander("🗂️ Regional Comparison — Box Plots", expanded=True):
        st.caption(
            "Box = IQR (25th–75th percentile). Line inside box = median. "
            "Whiskers extend to 1.5×IQR. Dots beyond whiskers = outliers. "
            "Lets you compare whether parameter values differ systematically across regions."
        )
        for param in available_params:
            plot_df = master[["Region", param]].dropna(subset=[param])
            if plot_df.empty:
                continue
            fig_box = px.box(
                plot_df,
                x="Region", y=param,
                color="Region",
                points="outliers",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title=param.replace("_", " "),
            )
            fig_box.update_traces(marker_size=3, line_width=1.2)
            apply_chart_theme(fig_box)
            fig_box.update_layout(
                height=320,
                showlegend=False,
                xaxis_title="",
                yaxis_title=param.replace("_", " "),
                margin=dict(t=40, b=30, l=50, r=10),
            )
            st.plotly_chart(fig_box, use_container_width=True)

    # ── 6e: Gender-stratified Comparison ─────────────────────────────────────
    with st.expander("⚧ Gender-stratified Comparison", expanded=False):
        st.caption(
            "Side-by-side box plots for Male vs Female per parameter. "
            "Many parameters (Haemoglobin, Iron, Creatinine, etc.) have known sex-based reference ranges — "
            "this plot helps verify whether your data reflects those expected differences."
        )
        valid_genders = master["Gender"].dropna().unique()
        valid_genders = [g for g in valid_genders if g not in ["Unknown", "nan"]]

        for param in available_params:
            plot_df = master[master["Gender"].isin(valid_genders)][["Gender", param]].dropna(subset=[param])
            if plot_df.empty:
                continue
            fig_sex = px.box(
                plot_df,
                x="Gender", y=param,
                color="Gender",
                points="outliers",
                color_discrete_map={"Male": "#5b9cf6", "Female": "#f472b6"},
                title=param.replace("_", " "),
            )
            fig_sex.update_traces(marker_size=3, line_width=1.2)
            apply_chart_theme(fig_sex)
            fig_sex.update_layout(
                height=300,
                showlegend=False,
                xaxis_title="",
                yaxis_title=param.replace("_", " "),
                margin=dict(t=40, b=20, l=50, r=10),
            )
            st.plotly_chart(fig_sex, use_container_width=True)

# =============================================================================
# SECTION 7 — DATA PIPELINE FLOW
# =============================================================================

section("⚙️ Data Pipeline")

pipeline_steps = [
    ("1", "16 ICMR\nCentres", "#3b82f6"),
    ("2", "PDF Lab\nReports", "#6366f1"),
    ("3", "Automated\nExtraction", "#8b5cf6"),
    ("4", "Structured\nDataset", "#a855f7"),
    ("5", "National\nDashboard", "#ec4899"),
]

fig_pipeline = go.Figure()

n = len(pipeline_steps)
for i, (num, label, color) in enumerate(pipeline_steps):
    x = i * 2

    # Box
    fig_pipeline.add_shape(
        type="rect", x0=x - 0.75, x1=x + 0.75, y0=0.2, y1=0.8,
        fillcolor=color, opacity=0.15, line_color=color, line_width=1.5,
    )

    # Step number
    fig_pipeline.add_annotation(
        x=x, y=0.7, text=f"<b>{num}</b>",
        showarrow=False, font=dict(size=13, color=color),
    )

    # Label
    fig_pipeline.add_annotation(
        x=x, y=0.42, text=label,
        showarrow=False, font=dict(size=10, color="#c8d4e4"),
        align="center",
    )

    # Arrow
    if i < n - 1:
        fig_pipeline.add_annotation(
            x=x + 0.9, y=0.5, ax=x + 0.75, ay=0.5,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.2,
            arrowcolor="#3b5a80", arrowwidth=1.5,
        )

fig_pipeline.update_layout(
    height=150,
    xaxis=dict(visible=False, range=[-1, (n - 1) * 2 + 1]),
    yaxis=dict(visible=False, range=[0, 1]),
    **CHART_THEME,
    margin=dict(t=10, b=10, l=10, r=10),
)
st.plotly_chart(fig_pipeline, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; font-size:0.75rem; color:#3a5070'>"
    "TERIIP Analytics Dashboard &nbsp;|&nbsp; ICMR &nbsp;|&nbsp; "
    f"Generated: {datetime.now().strftime('%d %b %Y')}"
    "</p>",
    unsafe_allow_html=True,
)
