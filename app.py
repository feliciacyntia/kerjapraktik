"""
Dashboard IPM vs Indeks Keparahan Kemiskinan (P2)
27 kabupaten/kota Jawa Barat, 2020–2025 — sumber: BPS Provinsi Jawa Barat.

Jalankan:  streamlit run app.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Konfigurasi
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPM vs P2 Jawa Barat",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_PATH = Path(__file__).parent / "data" / "master_ipm_p2_jabar_looker.csv"
DEFAULT_YEAR = 2025
ALL_LABEL = "Semua wilayah (rata-rata Jabar)"

INK = "#0F172A"
MUTED = "#64748B"
GRID = "#E2E8F0"
IPM_C = "#2563EB"   # biru  → IPM
P2_C = "#DC2626"    # merah → P2
OK_C = "#16A34A"
WARN_C = "#D97706"
HOVER_C = "#7C3AED"

STATUSES = ["Unggul", "Waspada kemiskinan", "Kejar IPM", "Tertinggal ganda"]
STATUS_COLORS = {
    "Unggul": OK_C,
    "Waspada kemiskinan": WARN_C,
    "Kejar IPM": IPM_C,
    "Tertinggal ganda": P2_C,
}
STATUS_DESC = {
    "Unggul": "IPM ≥ rata-rata & P2 ≤ rata-rata",
    "Waspada kemiskinan": "IPM ≥ rata-rata & P2 > rata-rata",
    "Kejar IPM": "IPM < rata-rata & P2 ≤ rata-rata",
    "Tertinggal ganda": "IPM < rata-rata & P2 > rata-rata",
}
FONT = "Inter, 'Segoe UI', system-ui, sans-serif"

# ─────────────────────────────────────────────────────────────────────────────
# Gaya (CSS)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,600&display=swap');
html, body, [class*="css"], .stMarkdown, .stText {{ font-family: {FONT}; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1400px; }}
#MainMenu, footer {{ visibility: hidden; }}

.hero {{
  position: relative; overflow: hidden; border-radius: 20px; padding: 28px 30px;
  border: 1px solid {GRID};
  background:
    radial-gradient(120% 140% at 0% 0%, rgba(37,99,235,.16) 0%, transparent 55%),
    radial-gradient(90% 120% at 100% 100%, rgba(220,38,38,.12) 0%, transparent 60%),
    #FFFFFF;
}}
.eyebrow {{ font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: {MUTED}; }}
.hero h1 {{ font-family: 'Fraunces', Georgia, serif; font-weight: 400; font-size: clamp(1.7rem, 3.4vw, 2.6rem);
  line-height: 1.12; margin: .35rem 0 .6rem; color: {INK}; letter-spacing: -.01em; }}
.hero h1 .ipm {{ color: {IPM_C}; }} .hero h1 .p2 {{ color: {P2_C}; }}
.hero p {{ font-size: 1rem; line-height: 1.6; max-width: none; margin: 0; color: {INK}; text-align: justify; }}

.kpi {{ position: relative; background: #fff; border: 1px solid {GRID}; border-radius: 16px;
  padding: 18px 18px 16px 22px; height: 100%; min-height: 182px; overflow: hidden;
  box-shadow: 0 1px 2px rgba(15,23,42,.04); }}
.kpi::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--accent); }}
.kpi .k {{ font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: {MUTED}; }}
.kpi .v {{ font-family: 'Fraunces', Georgia, serif; font-size: 2.5rem; line-height: 1.1; color: {INK}; margin: 6px 0 6px; }}
.kpi .vt {{ font-family: 'Fraunces', Georgia, serif; font-size: 1.6rem; line-height: 1.2; margin: 8px 0 8px; }}
.kpi .s {{ font-size: .8rem; color: {MUTED}; line-height: 1.45; margin-top: 6px; }}
.pill {{ display: inline-flex; gap: 6px; align-items: center; font-size: .78rem; font-weight: 600;
  padding: 3px 10px; border-radius: 999px; }}
.pill .d {{ font-weight: 400; color: {MUTED}; }}
.good {{ color: {OK_C}; background: rgba(22,163,74,.12); }}
.bad  {{ color: {P2_C}; background: rgba(220,38,38,.12); }}
.flat {{ color: {MUTED}; background: rgba(100,116,139,.12); }}

.card-title {{ font-size: 1.12rem; font-weight: 600; color: {INK}; margin: 0 0 2px; }}
.card-note {{ font-size: .82rem; color: {MUTED}; margin: 0 0 8px; line-height: 1.5; }}
.caveat {{ font-size: .82rem; line-height: 1.5; padding: 10px 12px; border-radius: 12px;
  background: rgba(217,119,6,.09); color: {INK}; margin-top: 8px; }}
.corr-r {{ font-family: 'Fraunces', Georgia, serif; font-size: 2.6rem; line-height: 1; }}
.legend-row {{ display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: .8rem; color: {MUTED}; margin-top: 4px; }}
.sw {{ display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}
.foot {{ font-size: .8rem; color: {MUTED}; line-height: 1.65; border-top: 1px solid {GRID}; padding-top: 14px; margin-top: 10px; }}
.foot b {{ color: {INK}; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 16px; }}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(src) -> pd.DataFrame:
    df = pd.read_csv(src, dtype={"kode_kabupaten_kota": str})
    latlon = df["koordinat"].astype(str).str.split(",", expand=True)
    df["lat"] = pd.to_numeric(latlon[0], errors="coerce")
    df["lon"] = pd.to_numeric(latlon[1], errors="coerce")
    df["tahun"] = df["tahun"].astype(int)
    ipm_hi = df["ipm"] >= df["ipm_rata2_jabar"]
    p2_lo = df["p2"] <= df["p2_rata2_jabar"]
    df["status"] = np.select(
        [ipm_hi & p2_lo, ipm_hi & ~p2_lo, ~ipm_hi & p2_lo],
        ["Unggul", "Waspada kemiskinan", "Kejar IPM"],
        default="Tertinggal ganda",
    )
    df["nama_pendek"] = df["nama_label"].str.replace(r"^Kab\.\s*", "", regex=True).str.replace(r"^Kota\s+", "Kt. ", regex=True)
    return df


def validate(df: pd.DataFrame) -> list[str]:
    issues = []
    if len(df) != 162:
        issues.append(f"Jumlah baris {len(df)} (diharapkan 162).")
    per_year = df.groupby("tahun").size()
    bad = per_year[per_year != 27]
    if not bad.empty:
        issues.append("Tahun dengan jumlah wilayah ≠ 27: " + ", ".join(f"{t} ({n})" for t, n in bad.items()))
    if df.duplicated(["kode_kabupaten_kota", "tahun"]).any():
        issues.append("Ada baris ganda untuk kombinasi wilayah–tahun yang sama.")
    return issues


@st.cache_data
def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Per tahun: n, korelasi Pearson r, garis tren, rata-rata (dari kolom file), jumlah tertinggal ganda."""
    out = []
    for t, g in df.groupby("tahun"):
        r = float(np.corrcoef(g["ipm"], g["p2"])[0, 1])
        slope, icpt = np.polyfit(g["ipm"], g["p2"], 1)
        out.append(
            dict(
                tahun=t, n=len(g), r=r, slope=float(slope), intercept=float(icpt),
                avg_ipm=g["ipm_rata2_jabar"].iloc[0], avg_p2=g["p2_rata2_jabar"].iloc[0],
                avg_ipm_yoy=g["ipm_jabar_yoy"].iloc[0], avg_p2_yoy=g["p2_jabar_yoy"].iloc[0],
                tertinggal=int((g["status"] == "Tertinggal ganda").sum()),
            )
        )
    return pd.DataFrame(out).set_index("tahun")


# Sumber data: file bawaan, atau unggahan bila file tidak ada
if DATA_PATH.exists():
    df = load_data(DATA_PATH)
else:
    up = st.file_uploader("Unggah master_ipm_p2_jabar_looker.csv", type="csv")
    if up is None:
        st.info("File data tidak ditemukan di folder `data/`. Unggah CSV untuk melanjutkan.")
        st.stop()
    df = load_data(up)

issues = validate(df)
summ = summarize(df)
YEARS = sorted(df["tahun"].unique().tolist())
REGION_NAMES = (
    df.drop_duplicates("kode_kabupaten_kota")
    .sort_values(["tipe", "nama_label"])["nama_label"].tolist()
)

# ─────────────────────────────────────────────────────────────────────────────
# Helper format
# ─────────────────────────────────────────────────────────────────────────────
def fx(v, d: int = 2) -> str:
    return "n/a" if v is None or pd.isna(v) else f"{v:.{d}f}"


def sg(v, d: int = 2) -> str:
    return "n/a" if v is None or pd.isna(v) else f"{v:+.{d}f}"


def tone(v, good_up: bool) -> str:
    if v is None or pd.isna(v) or v == 0:
        return "flat"
    return "good" if (v > 0) == good_up else "bad"


def delta_pill(v, good_up: bool, prev_year) -> str:
    if v is None or pd.isna(v):
        return '<span class="pill flat">■ n/a <span class="d">tidak ada tahun pembanding</span></span>'
    arrow = "■" if v == 0 else ("▲" if v > 0 else "▼")
    word = "" if v == 0 else (" · membaik" if (v > 0) == good_up else " · memburuk")
    return f'<span class="pill {tone(v, good_up)}">{arrow} {sg(v)} <span class="d">vs {prev_year}{word}</span></span>'


def strength(r: float) -> str:
    a = abs(r)
    return "sangat lemah" if a < 0.2 else "lemah" if a < 0.4 else "sedang" if a < 0.6 else "kuat" if a < 0.8 else "sangat kuat"


def base_layout(fig: go.Figure, height: int, **kw) -> go.Figure:
    fig.update_layout(
        height=height, template="plotly_white", font=dict(family=FONT, size=12, color=INK),
        margin=dict(l=8, r=8, t=8, b=8), hoverlabel=dict(bgcolor="white", font_size=12, font_family=FONT, bordercolor=GRID),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", **kw,
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# State & interaksi
# ─────────────────────────────────────────────────────────────────────────────
if "tahun" not in st.session_state:
    st.session_state["tahun"] = DEFAULT_YEAR if DEFAULT_YEAR in YEARS else YEARS[-1]
if "wilayah" not in st.session_state:
    st.session_state["wilayah"] = ALL_LABEL


def reset_filters():
    st.session_state["tahun"] = DEFAULT_YEAR if DEFAULT_YEAR in YEARS else YEARS[-1]
    st.session_state["wilayah"] = ALL_LABEL


def pick_from_chart(chart_key: str):
    """Klik titik di chart → sorot wilayah (klik wilayah yang sama lagi → batal)."""
    ev = st.session_state.get(chart_key)
    try:
        pts = ev["selection"]["points"]
    except (KeyError, TypeError):
        return
    if not pts:
        return
    cd = pts[0].get("customdata")
    name = cd[0] if isinstance(cd, (list, tuple)) else cd
    if name in REGION_NAMES:
        st.session_state["wilayah"] = ALL_LABEL if st.session_state.get("wilayah") == name else name


# ─────────────────────────────────────────────────────────────────────────────
# Kontrol
# ─────────────────────────────────────────────────────────────────────────────
hero_slot = st.empty()

with st.container(border=True):
    c1, c2, c3 = st.columns([3.2, 2.4, 1])
    with c1:
        tahun_pick = st.segmented_control("Tahun", YEARS, key="tahun", selection_mode="single")
    with c2:
        st.selectbox("Kabupaten/kota", [ALL_LABEL] + REGION_NAMES, key="wilayah")
    with c3:
        st.write("")
        st.button("↺ Atur ulang", on_click=reset_filters, use_container_width=True)

TAHUN = int(tahun_pick) if tahun_pick is not None else (DEFAULT_YEAR if DEFAULT_YEAR in YEARS else YEARS[-1])
WIL = None if st.session_state["wilayah"] == ALL_LABEL else st.session_state["wilayah"]
yi = YEARS.index(TAHUN)
PREV = YEARS[yi - 1] if yi > 0 else None
S = summ.loc[TAHUN]
yr = df[df["tahun"] == TAHUN].copy()
sel = yr[yr["nama_label"] == WIL].iloc[0] if WIL else None
r0 = summ.iloc[0]

# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
lede = (
    f"Pada <b>{TAHUN}</b>, rata-rata sederhana IPM kab/kota <b>{fx(S.avg_ipm)}</b>"
    + (f" ({sg(S.avg_ipm_yoy)} dari {PREV})" if PREV else "")
    + f" dan P2 <b>{fx(S.avg_p2)}</b>"
    + (f" ({sg(S.avg_p2_yoy)}, {'membaik' if S.avg_p2_yoy < 0 else 'memburuk' if S.avg_p2_yoy > 0 else 'tetap'})" if PREV else "")
    + f". Korelasi IPM–P2 <b>{S.r:.2f}</b> ({'negatif' if S.r < 0 else 'positif'} {strength(S.r)})"
    + (": wilayah ber-IPM tinggi cenderung punya kemiskinan yang lebih ringan, namun tidak selalu. " if S.r < 0 else ". ")
    + f"<b>{S.tertinggal}</b> wilayah tertinggal ganda (IPM di bawah dan P2 di atas rata-rata)."
)
hero_slot.markdown(
    f"""
<div class="hero">
  <div class="eyebrow">Jawa Barat · {int(S.n)} kabupaten/kota · {YEARS[0]}–{YEARS[-1]} · Sumber: BPS Jabar</div>
  <h1>Apakah <span class="ipm">IPM</span> yang tinggi berarti kemiskinan yang <span class="p2">lebih ringan</span>?</h1>
  <p>{lede}</p>
</div>
""",
    unsafe_allow_html=True,
)
for msg in issues:
    st.warning("Cek data: " + msg)

# ─────────────────────────────────────────────────────────────────────────────
# KPI
# ─────────────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
if sel is not None:
    ipm_v, ipm_d, p2_v, p2_d = sel.ipm, sel.ipm_yoy, sel.p2, sel.p2_yoy
    ipm_k, p2_k = f"IPM {TAHUN} · {WIL}", f"P2 {TAHUN} · {WIL}"
    ipm_s = f"Rata-rata Jabar {fx(S.avg_ipm)} · peringkat <b>{int(sel.rank_ipm)}</b> dari {int(S.n)} · {sel.kategori_ipm}"
    p2_s = f"Rata-rata Jabar {fx(S.avg_p2)} · peringkat keparahan <b>{int(sel.rank_p2)}</b> (1 = paling parah)"
else:
    ipm_v, ipm_d, p2_v, p2_d = S.avg_ipm, S.avg_ipm_yoy, S.avg_p2, S.avg_p2_yoy
    ipm_k, p2_k = f"IPM {TAHUN} · rata-rata Jabar", f"P2 {TAHUN} · rata-rata Jabar"
    ipm_s = "Indeks Pembangunan Manusia (kesehatan, pendidikan, daya beli). Rata-rata sederhana, bukan angka resmi."
    p2_s = "Indeks Keparahan Kemiskinan: ketimpangan pengeluaran di antara penduduk miskin. Makin rendah makin baik."

k1.markdown(f'<div class="kpi" style="--accent:{IPM_C}"><div class="k">{ipm_k}</div><div class="v">{fx(ipm_v)}</div>{delta_pill(ipm_d, True, PREV)}<div class="s">{ipm_s}</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi" style="--accent:{P2_C}"><div class="k">{p2_k}</div><div class="v">{fx(p2_v)}</div>{delta_pill(p2_d, False, PREV)}<div class="s">{p2_s}</div></div>', unsafe_allow_html=True)

trend_word = "menguat" if abs(S.r) > abs(r0.r) else "melemah" if abs(S.r) < abs(r0.r) else "tetap"
r_sub = (f"Pada {YEARS[0]}: <b>{r0.r:.2f}</b> → hubungan {trend_word}." if TAHUN != YEARS[0] else "Tahun awal periode.") + " Negatif = IPM tinggi beriringan dengan P2 rendah."
k3.markdown(f'<div class="kpi" style="--accent:{WARN_C}"><div class="k">Korelasi IPM–P2 (r) {TAHUN}</div><div class="v">{S.r:.2f}</div><span class="pill flat">{"negatif" if S.r < 0 else "positif"} {strength(S.r)}</span><div class="s">{r_sub}</div></div>', unsafe_allow_html=True)

if sel is not None:
    c = STATUS_COLORS[sel.status]
    k4.markdown(f'<div class="kpi" style="--accent:{c}"><div class="k">Status {TAHUN} · {WIL}</div><div class="vt" style="color:{c}">{sel.status}</div><div class="s">{STATUS_DESC[sel.status]} Jabar tahun yang sama.</div></div>', unsafe_allow_html=True)
else:
    names = ", ".join(yr.loc[yr["status"] == "Tertinggal ganda", "nama_pendek"]) or "—"
    k4.markdown(f'<div class="kpi" style="--accent:{P2_C}"><div class="k">Tertinggal ganda {TAHUN}</div><div class="v">{S.tertinggal}</div><div class="s">IPM di bawah & P2 di atas rata-rata: {names}.</div></div>', unsafe_allow_html=True)

st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# Peta + Korelasi
# ─────────────────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="medium")

with left:
    with st.container(border=True):
        st.markdown('<div class="card-title">Di mana wilayah yang tertinggal?</div><div class="card-note">Titik = pusat tiap kab/kota (bukan batas wilayah). Arahkan kursor untuk detail, klik untuk menyorot.</div>', unsafe_allow_html=True)
        mode = st.segmented_control("Warna peta", ["Status", "IPM", "P2"], default="Status", key="map_mode", label_visibility="collapsed") or "Status"
        fig = go.Figure()
        hover = (
            "<b>%{customdata[0]}</b><br>IPM %{customdata[1]:.2f} (%{customdata[2]})"
            "<br>P2 %{customdata[3]:.2f} (%{customdata[4]})<br>%{customdata[5]}<extra></extra>"
        )
        cd_cols = lambda d: np.stack([d["nama_label"], d["ipm"], d["ipm_yoy"].map(sg), d["p2"], d["p2_yoy"].map(sg), d["status"]], axis=-1)
        if sel is not None:
            fig.add_trace(go.Scattermap(lat=[sel.lat], lon=[sel.lon], mode="markers", marker=dict(size=34, color=INK, opacity=0.85), hoverinfo="skip", showlegend=False))
        sizes = lambda d: np.where(d["tipe"] == "Kota", 15, 21)
        if mode == "Status":
            for s in STATUSES:
                d = yr[yr["status"] == s]
                if d.empty:
                    continue
                fig.add_trace(go.Scattermap(lat=d["lat"], lon=d["lon"], mode="markers", name=s,
                                            marker=dict(size=sizes(d), color=STATUS_COLORS[s], opacity=0.9),
                                            customdata=cd_cols(d), hovertemplate=hover))
        else:
            col, scale, title = ("ipm", "Blues", "IPM") if mode == "IPM" else ("p2", "Reds", "P2 (makin merah makin parah)")
            fig.add_trace(go.Scattermap(lat=yr["lat"], lon=yr["lon"], mode="markers", name=mode,
                                        marker=dict(size=sizes(yr), color=yr[col], colorscale=scale, opacity=0.92, showscale=True,
                                                    colorbar=dict(title=dict(text=title, side="right"), thickness=10, len=0.7)),
                                        customdata=cd_cols(yr), hovertemplate=hover, showlegend=False))
        base_layout(fig, 470,
                    map=dict(style="carto-positron", center=dict(lat=float(df["lat"].mean()), lon=float(df["lon"].mean())), zoom=7.15),
                    legend=dict(orientation="h", y=0.01, x=0.01, bgcolor="rgba(255,255,255,.85)", bordercolor=GRID, borderwidth=1, font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True, key="map_chart", on_select=lambda: pick_from_chart("map_chart"),
                        selection_mode="points", config={"displayModeBar": False, "scrollZoom": True})

with right:
    with st.container(border=True):
        st.markdown('<div class="card-title">Apakah IPM tinggi beriringan dengan P2 rendah?</div><div class="card-note">Tiap titik satu kab/kota. Garis putus = rata-rata Jabar; garis miring = tren linear. Sumbu tetap di semua tahun agar bisa dibandingkan.</div>', unsafe_allow_html=True)
        tab_now, tab_anim = st.tabs([f"Tahun {TAHUN}", "▶ Animasi semua tahun"])
        xr = [df["ipm"].min() - 0.8, df["ipm"].max() + 0.8]
        yrng = [0, df["p2"].max() * 1.1]

        with tab_now:
            fig = go.Figure()
            fig.add_shape(type="rect", x0=xr[0], x1=S.avg_ipm, y0=S.avg_p2, y1=yrng[1], fillcolor=P2_C, opacity=0.07, line_width=0, layer="below")
            fig.add_shape(type="rect", x0=S.avg_ipm, x1=xr[1], y0=yrng[0], y1=S.avg_p2, fillcolor=OK_C, opacity=0.07, line_width=0, layer="below")
            fig.add_vline(x=S.avg_ipm, line=dict(color=MUTED, dash="dash", width=1))
            fig.add_hline(y=S.avg_p2, line=dict(color=MUTED, dash="dash", width=1))
            fig.add_annotation(x=xr[0], y=yrng[1], xanchor="left", yanchor="top", text="<b>Tertinggal ganda</b>", showarrow=False, font=dict(color=P2_C, size=11))
            fig.add_annotation(x=xr[1], y=yrng[0], xanchor="right", yanchor="bottom", text="<b>Unggul</b>", showarrow=False, font=dict(color=OK_C, size=11))
            xs = np.array([yr["ipm"].min(), yr["ipm"].max()])
            fig.add_trace(go.Scatter(x=xs, y=S.slope * xs + S.intercept, mode="lines", name="Tren linear",
                                     line=dict(color=INK, width=2, dash="dot"), hoverinfo="skip"))
            for s in STATUSES:
                d = yr[yr["status"] == s]
                if d.empty:
                    continue
                fig.add_trace(go.Scatter(
                    x=d["ipm"], y=d["p2"], mode="markers", name=s,
                    marker=dict(size=np.where(d["nama_label"] == WIL, 18, 12), color=STATUS_COLORS[s],
                                opacity=np.where((WIL is None) | (d["nama_label"] == WIL), 0.92, 0.3),
                                line=dict(color=np.where(d["nama_label"] == WIL, INK, "white").tolist(), width=np.where(d["nama_label"] == WIL, 2.5, 1.2).tolist())),
                    customdata=np.stack([d["nama_label"], d["rank_ipm"], d["rank_p2"]], axis=-1),
                    hovertemplate="<b>%{customdata[0]}</b><br>IPM %{x:.2f} · P2 %{y:.2f}<br>Rank IPM %{customdata[1]} · Rank P2 %{customdata[2]}<extra>" + s + "</extra>",
                ))
            if sel is not None:
                fig.add_annotation(x=sel.ipm, y=sel.p2, text=f"<b>{WIL}</b>", showarrow=True, arrowhead=0, ax=40, ay=-30,
                                   bgcolor="white", bordercolor=INK, borderwidth=1, font=dict(size=12))
            base_layout(fig, 400, legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=11)))
            fig.update_xaxes(title="IPM →", range=xr)
            fig.update_yaxes(title="P2 (lebih parah) ↑", range=yrng, tickformat=".2f")
            st.plotly_chart(fig, use_container_width=True, key="scatter_chart", on_select=lambda: pick_from_chart("scatter_chart"),
                            selection_mode="points", config={"displayModeBar": False})

        with tab_anim:
            fig = px.scatter(
                df.sort_values("tahun"), x="ipm", y="p2", animation_frame="tahun", animation_group="nama_label",
                color="status", color_discrete_map=STATUS_COLORS, category_orders={"status": STATUSES},
                hover_name="nama_label", range_x=xr, range_y=yrng,
                labels={"ipm": "IPM →", "p2": "P2 (lebih parah) ↑", "status": "", "tahun": "Tahun"},
            )
            fig.update_traces(marker=dict(size=12, line=dict(color="white", width=1)))
            base_layout(fig, 430, legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)))
            fig.update_layout(margin=dict(l=8, r=8, t=30, b=8))
            st.plotly_chart(fig, use_container_width=True, key="anim_chart", config={"displayModeBar": False})
            st.caption("Tekan ▶ untuk melihat pergerakan 2020–2025. Warna = status terhadap rata-rata Jabar tahun berjalan.")

        rc1, rc2 = st.columns([1, 3])
        with rc1:
            st.markdown(f'<div class="k" style="font-size:.72rem;color:{MUTED};letter-spacing:.08em">KORELASI r</div>'
                        f'<div class="corr-r" style="color:{OK_C if S.r < 0 else P2_C}">{S.r:.2f}</div>', unsafe_allow_html=True)
        with rc2:
            txt = (f"Hubungan <b>{'negatif' if S.r < 0 else 'positif'} {strength(S.r)}</b>"
                   + (": wilayah dengan IPM lebih tinggi cenderung memiliki P2 lebih rendah. " if S.r < 0 else ". ")
                   + f"Menurut garis tren, tiap +1 poin IPM berpadanan dengan perubahan P2 sekitar <b>{S.slope:+.4f}</b>. ")
            if TAHUN != YEARS[0]:
                txt += f"Dibanding {YEARS[0]} (r = {r0.r:.2f}), hubungan ini {trend_word}."
            st.markdown(f'<div style="font-size:.88rem;line-height:1.55">{txt}</div>'
                        f'<div class="caveat"><b>Korelasi bukan sebab-akibat.</b> IPM dan P2 bisa sama-sama dipengaruhi faktor lain '
                        f'(urbanisasi, struktur ekonomi, akses layanan). Dengan hanya {int(S.n)} wilayah, satu-dua wilayah ekstrem dapat menggeser r.</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="card-title" style="font-size:.95rem;margin-top:12px">Apakah hubungannya makin kuat dari tahun ke tahun?</div>', unsafe_allow_html=True)
        rb = summ.reset_index()
        fig = go.Figure(go.Bar(
            x=rb["tahun"].astype(str), y=rb["r"], text=rb["r"].map(lambda v: f"{v:.2f}"), textposition="outside",
            marker=dict(color=[IPM_C if t == TAHUN else "#CBD5E1" for t in rb["tahun"]], cornerradius=6),
            hovertemplate="%{x}: r = %{y:.2f}<extra></extra>",
        ))
        lo = min(0, rb["r"].min()) * 1.25
        hi = max(0, rb["r"].max()) * 1.25
        base_layout(fig, 170, bargap=0.45)
        fig.update_yaxes(range=[lo if lo < 0 else -0.05, hi if hi > 0 else 0.05], showticklabels=False, showgrid=False, zeroline=True, zerolinecolor=MUTED)
        fig.update_xaxes(type="category", side="top" if rb["r"].max() <= 0 else "bottom", showgrid=False)
        st.plotly_chart(fig, use_container_width=True, key="r_chart", config={"displayModeBar": False})

# ─────────────────────────────────────────────────────────────────────────────
# Tren
# ─────────────────────────────────────────────────────────────────────────────
def trend_fig(col: str, avg_col: str, yoy_col: str, good_up: bool, accent: str, dec: str) -> go.Figure:
    fig = go.Figure()
    fig.add_vrect(x0=TAHUN - 0.35, x1=TAHUN + 0.35, fillcolor=IPM_C, opacity=0.08, line_width=0, layer="below")
    for name, g in df.sort_values("tahun").groupby("nama_label"):
        if name == WIL:
            continue
        fig.add_trace(go.Scatter(
            x=g["tahun"], y=g[col], mode="lines", name=name, line=dict(color="#94A3B8", width=1.2),
            opacity=0.35 if WIL else 0.55, showlegend=False,
            customdata=np.stack([g["nama_label"], g[yoy_col].map(sg)], axis=-1),
            hovertemplate="<b>%{customdata[0]}</b><br>%{x}: %{y:" + dec + "} (Δ %{customdata[1]})<extra></extra>",
        ))
    avg = df.groupby("tahun")[avg_col].first()
    fig.add_trace(go.Scatter(x=avg.index, y=avg.values, mode="lines+markers", name="Rata-rata Jabar",
                             line=dict(color=INK, width=2.5, dash="dash"), marker=dict(size=6),
                             hovertemplate="<b>Rata-rata Jabar</b><br>%{x}: %{y:" + dec + "}<extra></extra>"))
    last = YEARS[-1]
    labels = [(avg.loc[last], f"Jabar {avg.loc[last]:{dec}}", INK)]
    if WIL:
        g = df[df["nama_label"] == WIL].sort_values("tahun")
        fig.add_trace(go.Scatter(
            x=g["tahun"], y=g[col], mode="lines+markers", name=WIL, line=dict(color=accent, width=3.5),
            marker=dict(size=np.where(g["tahun"] == TAHUN, 12, 7), color=accent, line=dict(color="white", width=1.5)),
            customdata=g[yoy_col].map(sg), hovertemplate="<b>" + WIL + "</b><br>%{x}: %{y:" + dec + "} (Δ %{customdata})<extra></extra>",
        ))
        v = g.loc[g["tahun"] == last, col].iloc[0]
        labels.append((v, f"{g['nama_pendek'].iloc[0]} {v:{dec}}", accent))
    # label ujung garis, dijaga agar tidak bertumpuk
    span = df[col].max() - df[col].min()
    labels.sort(key=lambda t: t[0])
    if len(labels) == 2 and abs(labels[1][0] - labels[0][0]) < span * 0.06:
        mid = (labels[0][0] + labels[1][0]) / 2
        labels = [(mid - span * 0.035, labels[0][1], labels[0][2]), (mid + span * 0.035, labels[1][1], labels[1][2])]
    for y, t, c in labels:
        fig.add_annotation(x=last, y=y, text=f"<b>{t}</b>", xanchor="left", xshift=10, showarrow=False, font=dict(color=c, size=11))
    base_layout(fig, 330, showlegend=False, hovermode="closest")
    fig.update_layout(margin=dict(l=8, r=110, t=8, b=8))
    fig.update_xaxes(tickmode="array", tickvals=YEARS, range=[YEARS[0] - 0.3, YEARS[-1] + 0.3], showgrid=False)
    fig.update_yaxes(tickformat=dec)
    return fig


with st.container(border=True):
    st.markdown(f'<div class="card-title">Apakah semua wilayah membaik sejak {YEARS[0]}?</div>'
                '<div class="card-note">Garis tipis = tiap kab/kota, garis putus = rata-rata sederhana Jabar, garis tebal = wilayah yang disorot. '
                'Semua tahun selalu ditampilkan; pita biru = tahun terpilih. Klik garis untuk menyorot wilayah.</div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2, gap="medium")
    with t1:
        st.markdown('**IPM** <span class="pill good">naik = membaik</span>', unsafe_allow_html=True)
        st.plotly_chart(trend_fig("ipm", "ipm_rata2_jabar", "ipm_yoy", True, IPM_C, ".2f"), use_container_width=True,
                        key="trend_ipm", on_select=lambda: pick_from_chart("trend_ipm"), selection_mode="points", config={"displayModeBar": False})
    with t2:
        st.markdown('**P2** <span class="pill good">turun = membaik</span>', unsafe_allow_html=True)
        st.plotly_chart(trend_fig("p2", "p2_rata2_jabar", "p2_yoy", False, P2_C, ".2f"), use_container_width=True,
                        key="trend_p2", on_select=lambda: pick_from_chart("trend_p2"), selection_mode="points", config={"displayModeBar": False})

# ─────────────────────────────────────────────────────────────────────────────
# Tabel peringkat
# ─────────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    h1, h2 = st.columns([3, 1.3])
    with h1:
        st.markdown(f'<div class="card-title">Bagaimana peringkat tiap kab/kota pada {TAHUN}?</div>'
                    '<div class="card-note">Klik judul kolom untuk mengurutkan. Δ = perubahan dari tahun sebelumnya. Rank P2: 1 = paling parah.</div>',
                    unsafe_allow_html=True)
    with h2:
        q = st.text_input("Cari", placeholder="Cari kab/kota…", label_visibility="collapsed")
    tb = yr.sort_values("rank_ipm")
    if q:
        tb = tb[tb["nama_label"].str.contains(q, case=False, regex=False)]

    def arrow_txt(v, good_up):
        if pd.isna(v):
            return "n/a"
        a = "■" if v == 0 else ("▲" if v > 0 else "▼")
        return f"{a} {v:+.2f}"

    show = pd.DataFrame({
        "Rank IPM": tb["rank_ipm"].astype(int),
        "Wilayah": tb["nama_label"],
        "IPM": tb["ipm"],
        "Δ IPM": [arrow_txt(v, True) for v in tb["ipm_yoy"]],
        "P2": tb["p2"],
        "Δ P2": [arrow_txt(v, False) for v in tb["p2_yoy"]],
        "Rank P2": tb["rank_p2"].astype(int),
        "Status": tb["status"],
        "Kategori IPM": tb["kategori_ipm"],
    })
    raw_ipm_yoy, raw_p2_yoy = tb["ipm_yoy"].tolist(), tb["p2_yoy"].tolist()

    def color_delta(series: pd.Series, raw: list, good_up: bool):
        out = []
        for v in raw:
            t = tone(v, good_up)
            out.append(f"color: {OK_C}; font-weight:600" if t == "good" else f"color: {P2_C}; font-weight:600" if t == "bad" else f"color: {MUTED}")
        return out

    styler = (
        show.style
        .apply(lambda s: color_delta(s, raw_ipm_yoy, True), subset=["Δ IPM"])
        .apply(lambda s: color_delta(s, raw_p2_yoy, False), subset=["Δ P2"])
        .map(lambda s: f"color: {STATUS_COLORS.get(s, MUTED)}; font-weight: 600", subset=["Status"])
        .apply(lambda row: ["background-color: rgba(37,99,235,.10)" if row["Wilayah"] == WIL else "" for _ in row], axis=1)
    )
    st.dataframe(
        styler, hide_index=True, use_container_width=True, height=min(38 * (len(show) + 1) + 4, 560),
        column_config={
            "IPM": st.column_config.ProgressColumn("IPM", min_value=float(np.floor(df["ipm"].min()) - 1), max_value=float(np.ceil(df["ipm"].max()) + 1), format="%.2f"),
            "P2": st.column_config.ProgressColumn("P2", min_value=0.0, max_value=float(df["p2"].max()), format="%.2f"),
            "Wilayah": st.column_config.TextColumn("Wilayah", width="medium"),
        },
    )
    st.download_button("⬇ Unduh data tahun ini (CSV)", yr.drop(columns=["lat", "lon", "nama_pendek"]).to_csv(index=False).encode("utf-8"),
                       file_name=f"ipm_p2_jabar_{TAHUN}.csv", mime="text/csv")

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="foot">
<b>Sumber data:</b> BPS Provinsi Jawa Barat — Indeks Pembangunan Manusia (IPM) dan Indeks Keparahan Kemiskinan (P2) menurut kabupaten/kota,
diolah dari file <i>master_ipm_p2_jabar_looker.csv</i> ({len(df)} baris, {df['kode_kabupaten_kota'].nunique()} wilayah, {YEARS[0]}–{YEARS[-1]}).<br>
<b>Rata-rata Jabar</b> = rata-rata sederhana {int(S.n)} kabupaten/kota (tidak dibobot jumlah penduduk) sebagaimana tercantum di file —
<b>bukan angka resmi</b> IPM/P2 Provinsi Jawa Barat dari BPS.<br>
<b>Metode:</b> korelasi Pearson (r) dan garis tren dihitung per tahun dari data file; korelasi tidak menunjukkan sebab-akibat.
Status: {' · '.join(f'<i>{s}</i> = {STATUS_DESC[s]}' for s in STATUSES)}. Δ dibanding tahun sebelumnya; tahun pertama tanpa pembanding (n/a).
Titik peta = koordinat pusat perkiraan, bukan batas wilayah resmi.
</div>
""",
    unsafe_allow_html=True,
)
