import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="PlayWise Pilot", layout="wide")

pd.options.display.float_format = "{:.2f}".format


def safe_read_excel(uploaded_file: bytes) -> pd.DataFrame:
    """Read the uploaded Excel file defensively so the app always boots."""

    try:
        df = pd.read_excel(uploaded_file)
    except Exception as exc:  # pragma: no cover - streamlit surface
        st.error(f"Could not read Excel file: {exc}")
        st.stop()

    return df

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
:root {
    --bg: #05070d;
    --card: #0a0f18;
    --stroke: #1c2331;
    --muted: #8ea2b5;
    --text: #e8edf4;
    --accent: #41f0c0;
    --glow-blue: rgba(0, 157, 255, 0.16);
    --glow-green: rgba(65, 240, 192, 0.22);
}
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
}
.app-wrapper {
    position: relative;
    isolation: isolate;
}
.main {
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at 20% 20%, rgba(65, 240, 192, 0.12), transparent 24%),
                radial-gradient(circle at 80% 0%, rgba(0, 157, 255, 0.1), transparent 23%),
                linear-gradient(135deg, #060910 0%, #070a12 50%, #05070d 100%);
}
.main:before {
    content: '';
    position: fixed;
    inset: -30% -20% 20% -20%;
    background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 70px 70px;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
    transform: perspective(1200px) rotateX(72deg) rotateZ(12deg) translate3d(-6%, -10%, 0);
    animation: gridDrift 24s linear infinite;
}
.main:after {
    content: '';
    position: fixed;
    inset: -10% -30% auto -30%;
    height: 80vh;
    background:
        radial-gradient(closest-side at 25% 35%, var(--glow-green), transparent 60%),
        radial-gradient(closest-side at 75% 60%, var(--glow-blue), transparent 55%),
        radial-gradient(closest-side at 45% 80%, rgba(255, 255, 255, 0.08), transparent 55%);
    filter: blur(12px);
    mix-blend-mode: screen;
    opacity: 0.9;
    pointer-events: none;
    z-index: 0;
    transform: perspective(1600px) rotateX(70deg) rotateZ(-6deg) translate3d(0, -10%, 0);
    animation: warpGlow 18s ease-in-out infinite alternate;
}
@keyframes gridDrift {
    0% {
        transform: perspective(1200px) rotateX(72deg) rotateZ(12deg) translate3d(-6%, -10%, 0);
    }
    50% {
        transform: perspective(1200px) rotateX(70deg) rotateZ(10deg) translate3d(4%, -6%, 0);
    }
    100% {
        transform: perspective(1200px) rotateX(68deg) rotateZ(6deg) translate3d(-8%, -12%, 0);
    }
}
@keyframes warpGlow {
    0% {
        transform: perspective(1600px) rotateX(70deg) rotateZ(-6deg) translate3d(0, -10%, 0);
    }
    50% {
        transform: perspective(1600px) rotateX(68deg) rotateZ(-2deg) translate3d(3%, -4%, 0);
    }
    100% {
        transform: perspective(1600px) rotateX(66deg) rotateZ(2deg) translate3d(-3%, -12%, 0);
    }
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11,16,26,0.95), rgba(6,9,15,0.96));
    border-right: 1px solid var(--stroke);
    box-shadow: 8px 0 30px rgba(0,0,0,0.45);
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-weight: 800 !important;
    letter-spacing: 0.08em;
    font-size: 1.05rem !important;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .st-emotion-cache-1q7ch1g p {
    color: var(--muted);
}
h1 {
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    letter-spacing: 0.04em;
    margin-bottom: 0.15rem;
}
.page-wrap {
    max-width: 1180px;
    margin: 0 auto;
    padding: 22px 14px 0 14px;
}
.hero-copy {
    position: relative;
    z-index: 2;
}
.upload-col {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.18), rgba(0, 167, 255, 0.18));
    color: #9bf6da;
    border: 1px solid rgba(65, 240, 192, 0.45);
}
.playwise-subtitle {
    font-size: 0.97rem;
    color: var(--muted);
    margin-bottom: 0.75rem;
}
.hero-headline {
    font-size: 1.45rem;
    margin-bottom: 0.3rem;
    font-weight: 700;
}
.hero-description {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.65;
    max-width: 640px;
    margin-bottom: 0.6rem;
}
.hero-bullets {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 8px;
}
.hero-bullets li {
    position: relative;
    padding-left: 18px;
    color: var(--text);
}
.hero-bullets li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--accent);
}
.upload-card {
    position: relative;
    background: radial-gradient(120% 160% at 0% 0%, rgba(65, 240, 192, 0.08), rgba(10, 15, 24, 0.9)),
                radial-gradient(140% 160% at 100% 0%, rgba(0, 167, 255, 0.1), rgba(10, 15, 24, 0.9)),
                var(--card);
    border: 1px solid var(--stroke);
    border-radius: 20px;
    padding: 18px;
    box-shadow:
        0 26px 80px rgba(0,0,0,0.7),
        0 12px 30px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.04);
}
.upload-card__inner {
    background: linear-gradient(160deg, rgba(255,255,255,0.03), rgba(255,255,255,0));
    border-radius: 14px;
    padding: 10px 12px 6px 12px;
    border: 1px solid rgba(255,255,255,0.04);
}
.upload-card__title {
    font-weight: 800;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}
.upload-card__helper {
    margin: 0 0 6px 0;
    color: var(--muted);
    font-size: 0.9rem;
}
.hero-spacer {
    height: 32px;
}
.hero-card {
    position: relative;
    overflow: hidden;
    background: var(--card);
    border-radius: 18px;
    padding: 22px 24px 20px 24px;
    border: 1px solid var(--stroke);
    box-shadow: 0 24px 70px rgba(0,0,0,0.6);
}
.hero-card:before {
    content: '';
    position: absolute;
    inset: -10% auto auto -10%;
    width: 40%;
    height: 40%;
    background: radial-gradient(circle, rgba(65, 240, 192, 0.16), transparent 65%);
    filter: blur(6px);
}
.hero-card:after {
    content: '';
    position: absolute;
    inset: auto -30% -30% auto;
    width: 35%;
    height: 35%;
    background: radial-gradient(circle, rgba(0, 167, 255, 0.16), transparent 60%);
    filter: blur(10px);
}
.hero-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-top: 14px;
    position: relative;
    z-index: 1;
}
.hero-grid__item {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 10px 12px;
}
.hero-label {
    display: block;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
}
.hero-value {
    font-weight: 700;
    color: var(--text);
}
.element-container:has(div[data-testid="metric-container"]) {
    background: rgba(11,16,26,0.9);
    border-radius: 14px;
    padding: 14px 14px 10px 14px;
    border: 1px solid var(--stroke);
    box-shadow: 0 6px 18px rgba(0,0,0,0.55);
    transition: all 0.12s ease;
}
.element-container:has(div[data-testid="metric-container"]):hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 26px rgba(0,0,0,0.65);
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    letter-spacing: 0.02em;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 800 !important;
}
.section-stack {
    display: grid;
    gap: 16px;
    margin-top: 10px;
}
.section-card {
    position: relative;
    background: radial-gradient(120% 160% at 0% 0%, rgba(65, 240, 192, 0.08), rgba(10, 15, 24, 0.92)),
                radial-gradient(140% 160% at 100% 0%, rgba(0, 167, 255, 0.12), rgba(10, 15, 24, 0.92)),
                rgba(8, 11, 18, 0.96);
    border: 1px solid var(--stroke);
    border-radius: 18px;
    padding: 14px 14px 10px 14px;
    box-shadow:
        0 26px 80px rgba(0,0,0,0.7),
        0 12px 30px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.04);
}
.section-card .stExpander {
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: rgba(255,255,255,0.02) !important;
    border-radius: 14px !important;
}
.section-card details summary {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text);
}
.section-card details summary::marker {
    color: var(--accent);
    font-size: 1.2rem;
}
div[data-testid="dataframe"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--stroke);
    margin-top: 10px;
    background: rgba(10, 15, 24, 0.9);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}
.stDataFrame thead tr { background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0)); }
.stDataFrame tbody tr:nth-child(even) { background: rgba(255,255,255,0.02); }
.stDataFrame tbody tr:hover { background: rgba(65, 240, 192, 0.06); }
.data-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    font-size: 0.9rem;
    color: var(--text);
}
.data-chip__dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--accent);
    box-shadow: 0 0 10px rgba(65, 240, 192, 0.6);
}
.digest-row {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 8px;
}
.digest-chip {
    flex: 1 1 200px;
    min-width: 200px;
    background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid var(--stroke);
    border-radius: 14px;
    padding: 14px 16px 12px 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.55);
}
.digest-label {
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
}
.digest-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 8px;
}
.digest-value .win { color: var(--accent); }
.digest-value .loss { color: #ff7b7b; }
.stExpander {
    border-radius: 12px !important;
    border: 1px solid var(--stroke) !important;
    background: rgba(7,10,16,0.8) !important;
}
h3, h4 {
    font-weight: 700 !important;
}
.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.15), rgba(0, 167, 255, 0.15));
    color: #9bf6da;
    border: 1px solid rgba(65, 240, 192, 0.45);
    margin-bottom: 8px;
}
.stFileUploader div[data-testid="stFileUploaderDropzone"] {
    border: 1px dashed var(--stroke);
    background: rgba(255,255,255,0.02);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
hero_cols = st.columns([1.05, 0.95])

with hero_cols[0]:
    st.markdown(
        """
        <div class="hero-copy">
            <div class="hero-pill">PlayWise · pilot build</div>
            <h1 style="margin-top:6px;">PlayWise</h1>
            <p class="playwise-subtitle">Use your strengths, learn from your weaknesses.</p>
            <h3 class="hero-headline">See what’s working — and what’s not</h3>
            <p class="hero-description">Upload your bets to get ROI, profit trends and a profile of how you play. No tips, no picks — just the stats that show your edge.</p>
            <ul class="hero-bullets">
                <li>ROI & profit curve to show momentum</li>
                <li>Strongest and weakest markets surfaced automatically</li>
                <li>Single- vs combo-heavy profile at a glance</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_cols[1]:
    st.markdown("<div class='upload-col'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="upload-card">
            <div class="upload-card__inner">
                <div class="upload-card__title">Upload Sportsbook Excel</div>
                <p class="upload-card__helper">.xlsx export from e.g. Coolbet or Veikkaus.</p>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("", type=["xlsx"])
    st.caption("Tip: export your betting history as .xlsx and drop it here.")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-spacer'></div>", unsafe_allow_html=True)

if uploaded_file is None:
    st.stop()

# ---------- DATA PROCESSING ----------
df = safe_read_excel(uploaded_file)
required_cols = {"date", "rank", "ticket type", "product", "bets", "wins", "odds"}

if not required_cols.issubset(df.columns):
    st.error("Missing required columns in Excel. Need at least: date, rank, ticket type, product, bets, wins, odds.")
    st.stop()

df["ticket type"] = df["ticket type"].astype(str)
df["product"] = df["product"].astype(str)
df["date"] = pd.to_datetime(df["date"].ffill())
df["rank"] = df["rank"].ffill()

if "market name" in df.columns:
    def classify_market(m):
        m = str(m).lower()
        if any(k in m for k in ["over/under goals", "over under goals", "total goals", "goal line", "goals line", "goals over", "goals under"]):
            return "Over/Under Goals"
        if any(k in m for k in ["player", "points", "pts", "rebounds", "assists", "steals", "blocks", "shots"]):
            return "Player Points"
        if any(k in m for k in ["1x2", "match result", "full time result", "moneyline", "winner", "to win"]):
            return "Match Results"
        return "Other Markets"

    df["market_group"] = df["market name"].apply(classify_market)

if "market name" in df.columns:
    def classify_market(m):
        m = str(m).lower()
        if any(k in m for k in ["over/under goals", "over under goals", "total goals", "goal line", "goals line", "goals over", "goals under"]):
            return "Over/Under Goals"
        if any(k in m for k in ["player", "points", "pts", "rebounds", "assists", "steals", "blocks", "shots"]):
            return "Player Points"
        if any(k in m for k in ["1x2", "match result", "full time result", "moneyline", "winner", "to win"]):
            return "Match Results"
        return "Other Markets"

    df["market_group"] = df["market name"].apply(classify_market)

if "market name" in df.columns:
    def classify_market(m):
        m = str(m).lower()
        if any(k in m for k in ["over/under goals", "over under goals", "total goals", "goal line", "goals line", "goals over", "goals under"]):
            return "Over/Under Goals"
        if any(k in m for k in ["player", "points", "pts", "rebounds", "assists", "steals", "blocks", "shots"]):
            return "Player Points"
        if any(k in m for k in ["1x2", "match result", "full time result", "moneyline", "winner", "to win"]):
            return "Match Results"
        return "Other Markets"

    df["market_group"] = df["market name"].apply(classify_market)

if "market name" in df.columns:
    def classify_market(m):
        m = str(m).lower()
        if any(k in m for k in ["over/under goals", "over under goals", "total goals", "goal line", "goals line", "goals over", "goals under"]):
            return "Over/Under Goals"
        if any(k in m for k in ["player", "points", "pts", "rebounds", "assists", "steals", "blocks", "shots"]):
            return "Player Points"
        if any(k in m for k in ["1x2", "match result", "full time result", "moneyline", "winner", "to win"]):
            return "Match Results"
        return "Other Markets"

    df["market_group"] = df["market name"].apply(classify_market)

df_grouped = (
    df.groupby(["date", "rank", "ticket type", "product"], as_index=False)
      .agg(
          bets=("bets", "sum"),
          wins=("wins", "sum"),
          total_odds=("odds", np.prod),
          legs=("odds", "size")
      )
)

df_grouped["Profit"] = df_grouped["wins"] - df_grouped["bets"]
df_grouped["ROI %"] = np.where(
    df_grouped["bets"] > 0,
    (df_grouped["Profit"] / df_grouped["bets"]) * 100,
    0.0,
)

# short circuit if there's nothing to show, preventing downstream styler errors
if df_grouped.empty:
    st.warning("No rows found in the uploaded file. Add bets to see analytics.")
    st.stop()

# --- ROUND NUMERIC COLUMNS TO 2 DECIMALS ---
numeric_cols_grouped = df_grouped.select_dtypes(include="number").columns
df_grouped[numeric_cols_grouped] = df_grouped[numeric_cols_grouped].round(2)

df_filtered = df_grouped.copy()
df_filtered_raw = df.copy()

def color_roi(v):
    if pd.isna(v): return ""
    return "color: green" if v > 0 else "color: red" if v < 0 else "color: gray"


# ---------- HERO OVERVIEW CARD ----------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown('<div class="section-pill">OVERVIEW</div>', unsafe_allow_html=True)
top_cols = st.columns([2, 1.3])

with top_cols[0]:
    range_options = {
        "1 Month": pd.DateOffset(months=1),
        "3 Months": pd.DateOffset(months=3),
        "6 Months": pd.DateOffset(months=6),
        "1 Year": pd.DateOffset(years=1),
        "All Time": None,
    }
    default_range = list(range_options.keys()).index("All Time")
    selected_range = st.radio(
        "Timeline",
        list(range_options.keys()),
        horizontal=True,
        index=default_range,
    )

    cutoff = range_options[selected_range]
    if cutoff is not None:
        min_date = df_grouped["date"].max() - cutoff
        df_filtered = df_grouped[df_grouped["date"] >= min_date].copy()
        df_filtered_raw = df[df["date"] >= min_date].copy()
    else:
        df_filtered = df_grouped.copy()
        df_filtered_raw = df.copy()

    if df_filtered.empty:
        st.warning("No bets found for this timeline.")
        st.stop()

    total_stake = float(df_filtered["bets"].sum())
    total_return = float(df_filtered["wins"].sum())
    total_profit = total_return - total_stake
    roi_total = (total_profit / total_stake * 100) if total_stake > 0 else 0.0
    avg_bet = float(df_filtered["bets"].mean())
    num_bets = len(df_filtered)
    num_singles = int((df_filtered["ticket type"].str.lower() == "single").sum())
    num_combos = int((df_filtered["ticket type"].str.lower() == "combo").sum())

    total_stake = round(total_stake, 2)
    total_return = round(total_return, 2)
    total_profit = round(total_profit, 2)
    roi_total = round(roi_total, 2)
    avg_bet = round(avg_bet, 2)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("ROI %", f"{roi_total:.2f}%")
    mc2.metric("Total Profit", f"{total_profit:.2f} €")
    mc3.metric("Avg Bet", f"{avg_bet:.2f} €")
    mc4.metric("Tickets", f"{num_bets} ({num_singles}/{num_combos})")

    st.markdown("##### Profit over time")
    df_daily = df_filtered.groupby("date", as_index=False)["Profit"].sum().sort_values("date")
    df_daily["Profit"] = df_daily["Profit"].round(2)

    if not df_daily.empty:
        df_range = df_daily.copy()
        if cutoff is not None:
            min_date = df_daily["date"].max() - cutoff
            df_range = df_daily[df_daily["date"] >= min_date].copy()

        df_range["CumProfit"] = df_range["Profit"].cumsum().round(2)
        df_range["Profit"] = df_range["Profit"].round(2)

        chart = alt.Chart(df_range).mark_line().encode(
            x="date:T",
            y="CumProfit:Q"
        )
        st.altair_chart(chart, use_container_width=True)

by_product = (
    df_filtered.groupby("product")
    .agg(stake=("bets","sum"), ret=("wins","sum"))
    .assign(
        profit=lambda x: x["ret"] - x["stake"],
        roi=lambda x: np.where(x["stake"] > 0, (x["ret"]-x["stake"]) / x["stake"] * 100, 0.0)
    )
)

by_ticket = (
    df_filtered.groupby("ticket type")
    .agg(stake=("bets","sum"), ret=("wins","sum"))
    .assign(
        profit=lambda x: x["ret"] - x["stake"],
        roi=lambda x: np.where(x["stake"] > 0, (x["ret"]-x["stake"]) / x["stake"] * 100, 0.0)
    )
)

by_market_group = None
if "market_group" in df_filtered_raw.columns:
    by_market_group = (
        df_filtered_raw.groupby("market_group")
        .agg(stake=("bets","sum"), ret=("wins","sum"))
        .assign(
            profit=lambda x: x["ret"] - x["stake"],
            roi=lambda x: np.where(x["stake"] > 0, (x["ret"]-x["stake"]) / x["stake"] * 100, 0.0)
        )
        .sort_values("roi", ascending=False)
    )

# ROUND GROUPED TABLES
by_product_num_cols = by_product.select_dtypes(include="number").columns
by_ticket_num_cols = by_ticket.select_dtypes(include="number").columns
by_product[by_product_num_cols] = by_product[by_product_num_cols].round(2)
by_ticket[by_ticket_num_cols] = by_ticket[by_ticket_num_cols].round(2)

if by_market_group is not None:
    by_market_num_cols = by_market_group.select_dtypes(include="number").columns
    by_market_group[by_market_num_cols] = by_market_group[by_market_num_cols].round(2)

with top_cols[1]:
    st.markdown("##### Quick profile")
    avg_legs = df_filtered["legs"].mean()

    if avg_legs > 1.5:
        st.write("🎲 You lean **combo-heavy** → higher variance, bigger swings.")
    else:
        st.write("🎯 You lean **single-heavy** → more stable, lower variance.")

    if by_market_group is not None and not by_market_group.empty:
        best = by_market_group["roi"].idxmax()
        st.write(f"📈 Strongest edge in **{best}** ({by_market_group.loc[best, 'roi']:.2f}%).")
        losing = by_market_group[by_market_group["roi"] < 0]
        if not losing.empty:
            worst = by_market_group["roi"].idxmin()
            st.write(f"📉 Weakest in **{worst}** ({by_market_group.loc[worst, 'roi']:.2f}%).")
    else:
        st.write("ℹ️ Add more bets to unlock market insights.")

    if total_stake > 0:
        st.write(f"💶 Total volume tracked: **{total_stake:.2f} €**")

st.markdown('</div>', unsafe_allow_html=True)  # end hero-card


# ---------- QUICK DIGEST ----------
date_start = df_grouped["date"].min()
date_end = df_grouped["date"].max()
win_rate = round((df_grouped["wins"] > 0).mean() * 100, 1)
loss_rate = round(100 - win_rate, 1)

digest_cols = st.columns([1.4, 1])

with digest_cols[0]:
    st.markdown("#### Session digest")
    st.markdown(
        """
        <div class="digest-row">
            <div class="digest-chip">
                <div class="digest-label">Bets</div>
                <div class="digest-value">{rows}</div>
            </div>
            <div class="digest-chip">
                <div class="digest-label">Period</div>
                <div class="digest-value">{start} → {end}</div>
            </div>
            <div class="digest-chip">
                <div class="digest-label">Win / Loss</div>
                <div class="digest-value"><span class="win">{win}%</span><span class="loss">{loss}%</span></div>
            </div>
        </div>
        """.format(
            rows=len(df_grouped),
            start=date_start.strftime("%d %b %Y") if pd.notna(date_start) else "–",
            end=date_end.strftime("%d %b %Y") if pd.notna(date_end) else "–",
            win=win_rate,
            loss=loss_rate,
        ),
        unsafe_allow_html=True,
    )

with digest_cols[1]:
    st.markdown("#### Micro-highlights")
    if by_product is not None and not by_product.empty:
        best_product = by_product["roi"].idxmax()
        st.write(f"✅ Strongest lane: **{best_product}** ({by_product.loc[best_product, 'roi']:.2f}% ROI)")
    if by_product is not None and not by_product.empty:
        worst_product = by_product["roi"].idxmin()
        st.write(f"⚠️ Watchlist: **{worst_product}** ({by_product.loc[worst_product, 'roi']:.2f}% ROI)")
    st.write(f"🧮 Mean stake per ticket: **{avg_bet:.2f} €**")


# ---------- INTERACTIVE SECTIONS ----------

st.markdown("### Deep dives")
st.markdown("<div class='section-stack'>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
with st.expander("📊 Markets — click to open full view", expanded=False):
    st.markdown("#### Profitability By Market Group")
    if by_market_group is not None and not by_market_group.empty:
        display_by_market = by_market_group.copy()
        display_by_market.index = display_by_market.index.str.title()
        display_by_market = display_by_market.rename(
            columns={
                "stake": "Stake",
                "ret": "Return",
                "profit": "Profit",
                "roi": "ROI %",
            }
        )[ ["Stake", "Return", "Profit", "ROI %"] ]
        formatter_market = {col: "{:.2f}" for col in display_by_market.select_dtypes(include="number").columns}
        st.dataframe(
            display_by_market.style
                .applymap(color_roi, subset=["ROI %"])
                .format(formatter_market),
            use_container_width=True
        )
    else:
        st.info("No market data found in this file (missing 'market name').")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
with st.expander("🎟 Tickets — click to open full view", expanded=False):
    st.markdown("#### Live Vs Prematch")
    display_by_product = by_product.copy()
    display_by_product.index = display_by_product.index.str.title()
    display_by_product = display_by_product.rename(
        columns={
            "stake": "Stake",
            "ret": "Return",
            "profit": "Profit",
            "roi": "ROI %",
        }
    )[ ["Stake", "Return", "Profit", "ROI %"] ]
    formatter_prod = {col: "{:.2f}" for col in display_by_product.select_dtypes(include="number").columns}
    st.dataframe(
        display_by_product.style
            .applymap(color_roi, subset=["ROI %"])
            .format(formatter_prod),
        use_container_width=True
    )

    st.markdown("#### Combo Vs Single")
    display_by_ticket = by_ticket.copy()
    display_by_ticket.index = display_by_ticket.index.str.title()
    display_by_ticket = display_by_ticket.rename(
        columns={
            "stake": "Stake",
            "ret": "Return",
            "profit": "Profit",
            "roi": "ROI %",
        }
    )[ ["Stake", "Return", "Profit", "ROI %"] ]
    formatter_ticket = {col: "{:.2f}" for col in display_by_ticket.select_dtypes(include="number").columns}
    st.dataframe(
        display_by_ticket.style
            .applymap(color_roi, subset=["ROI %"])
            .format(formatter_ticket),
        use_container_width=True
    )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
with st.expander("📄 Raw Data — click to open full view", expanded=False):
    display_grouped = df_grouped.copy()
    display_grouped = display_grouped.rename(
        columns={
            "date": "Date",
            "rank": "Rank",
            "ticket type": "Ticket Type",
            "product": "Product",
            "bets": "Bets",
            "wins": "Wins",
            "total_odds": "Total Odds",
            "legs": "Legs",
        }
    )
    num_cols_grouped = display_grouped.select_dtypes(include="number").columns
    formatter_grouped = {col: "{:.2f}" for col in num_cols_grouped}
    st.dataframe(
        display_grouped.style.format(formatter_grouped),
        use_container_width=True
    )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)



