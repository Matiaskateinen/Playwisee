import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="PlayWise Pilot", layout="wide")

pd.options.display.float_format = "{:.2f}".format

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
    background: radial-gradient(circle at 20% 20%, rgba(65, 240, 192, 0.12), transparent 24%),
                radial-gradient(circle at 80% 0%, rgba(0, 157, 255, 0.1), transparent 23%),
                linear-gradient(135deg, #060910 0%, #070a12 50%, #05070d 100%);
}
.main:before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 60px 60px;
    opacity: 0.5;
    pointer-events: none;
    z-index: 0;
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
.playwise-subtitle {
    font-size: 0.97rem;
    color: var(--muted);
    margin-bottom: 0.75rem;
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
.stTabs [role="tab"] {
    padding: 10px 22px;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--muted);
    border-bottom: 2px solid transparent;
}
.stTabs [role="tab"][aria-selected="true"] {
    border-bottom: 3px solid var(--accent);
    color: var(--text);
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

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### PLAYWISE")
    st.caption("Betting performance cockpit")

    uploaded_file = st.file_uploader("Upload Sportsbook Excel", type=["xlsx"])

    st.markdown("---")
    st.caption("Tip: export from Veikkaus as `.xlsx` and drop it here.")

# ---------- MAIN ----------
st.title("PlayWise Pilot")
st.markdown(
    '<p class="playwise-subtitle">Precision-grade cockpit for disciplined bettors.</p>',
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="section-pill">Setup</div>
            <h3 style="margin-top:4px; margin-bottom:6px;">Import and get a lab-grade view of your betting</h3>
            <p style="opacity:0.82; font-size:0.95rem; max-width:520px; line-height:1.55;">
                Drop a Sportsbook Excel export in the sidebar. PlayWise cleans, aggregates and serves
                a clinical read on your bankroll movement: ROI, profit velocity, edge pockets and your
                behavioural profile.
            </p>
            <div class="hero-grid">
                <div class="hero-grid__item">
                    <span class="hero-label">Format</span>
                    <span class="hero-value">.xlsx (Veikkaus)</span>
                </div>
                <div class="hero-grid__item">
                    <span class="hero-label">Insights</span>
                    <span class="hero-value">ROI, profit, markets</span>
                </div>
                <div class="hero-grid__item">
                    <span class="hero-label">Profile</span>
                    <span class="hero-value">Singles vs combos</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ---------- DATA PROCESSING ----------
df = pd.read_excel(uploaded_file)
required_cols = {"date", "rank", "ticket type", "product", "bets", "wins", "odds"}

if not required_cols.issubset(df.columns):
    st.error("Missing required columns in Excel. Need at least: date, rank, ticket type, product, bets, wins, odds.")
    st.stop()

df["ticket type"] = df["ticket type"].astype(str)
df["product"] = df["product"].astype(str)
df["date"] = pd.to_datetime(df["date"].ffill())
df["rank"] = df["rank"].ffill()

df_grouped = (
    df.groupby(["date", "rank", "ticket type", "product"], as_index=False)
      .agg(
          bets=("bets", "sum"),
          wins=("wins", "sum"),
          total_odds=("odds", np.prod),
          legs=("odds", "size")
      )
)

df_grouped["combo_label"] = df_grouped.apply(
    lambda row: (
        f"combo {row['date'].strftime('%d/%m')}"
        if (row["ticket type"].lower().startswith("combo") and pd.notna(row["date"]))
        else ""
    ),
    axis=1
)

df_grouped["Profit"] = df_grouped["wins"] - df_grouped["bets"]
df_grouped["ROI %"] = (df_grouped["Profit"] / df_grouped["bets"]) * 100

# --- ROUND NUMERIC COLUMNS TO 2 DECIMALS ---
numeric_cols_grouped = df_grouped.select_dtypes(include="number").columns
df_grouped[numeric_cols_grouped] = df_grouped[numeric_cols_grouped].round(2)

total_stake = float(df_grouped["bets"].sum())
total_return = float(df_grouped["wins"].sum())
total_profit = total_return - total_stake
roi_total = (total_profit / total_stake * 100) if total_stake > 0 else 0.0
avg_bet = float(df_grouped["bets"].mean())
num_bets = len(df_grouped)
num_singles = int((df_grouped["ticket type"].str.lower() == "single").sum())
num_combos = int((df_grouped["ticket type"].str.lower() == "combo").sum())

total_stake = round(total_stake, 2)
total_return = round(total_return, 2)
total_profit = round(total_profit, 2)
roi_total = round(roi_total, 2)
avg_bet = round(avg_bet, 2)

by_product = (
    df_grouped.groupby("product")
    .agg(stake=("bets","sum"), ret=("wins","sum"))
    .assign(roi=lambda x: (x["ret"]-x["stake"]) / x["stake"] * 100)
)

by_ticket = (
    df_grouped.groupby("ticket type")
    .agg(stake=("bets","sum"), ret=("wins","sum"))
    .assign(roi=lambda x: (x["ret"]-x["stake"]) / x["stake"] * 100)
)

by_market_group = None
if "market name" in df.columns:
    def classify_market(m):
        m = str(m).lower()
        if any(k in m for k in ["player","points","pts","rebounds","assists","steals","blocks","shots","goal"]):
            return "Player props"
        if any(k in m for k in ["1x2","match result","full time result"]):
            return "Match result (1X2)"
        if any(k in m for k in ["moneyline","winner","to win"]):
            return "Moneyline"
        if any(k in m for k in ["over","under","total goals","total points"]):
            return "Totals (over/under)"
        return "Other markets"

    df["market_group"] = df["market name"].apply(classify_market)

    by_market_group = (
        df.groupby("market_group")
        .agg(stake=("bets","sum"), ret=("wins","sum"))
        .assign(roi=lambda x: (x["ret"]-x["stake"]) / x["stake"] * 100)
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

def color_roi(v):
    if pd.isna(v): return ""
    return "color: green" if v > 0 else "color: red" if v < 0 else "color: gray"


# ---------- HERO OVERVIEW CARD ----------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown('<div class="section-pill">OVERVIEW</div>', unsafe_allow_html=True)
top_cols = st.columns([2, 1.3])

with top_cols[0]:
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("ROI %", f"{roi_total:.2f}%")
    mc2.metric("Total Profit", f"{total_profit:.2f} €")
    mc3.metric("Avg Bet", f"{avg_bet:.2f} €")
    mc4.metric("Tickets", f"{num_bets} ({num_singles}/{num_combos})")

    st.markdown("##### Profit over time")
    df_daily = df_grouped.groupby("date", as_index=False)["Profit"].sum().sort_values("date")
    df_daily["CumProfit"] = df_daily["Profit"].cumsum()
    df_daily["Profit"] = df_daily["Profit"].round(2)
    df_daily["CumProfit"] = df_daily["CumProfit"].round(2)

    if not df_daily.empty:
        chart = alt.Chart(df_daily).mark_line().encode(
            x="date:T",
            y="CumProfit:Q"
        )
        st.altair_chart(chart, use_container_width=True)

with top_cols[1]:
    st.markdown("##### Quick profile")
    avg_legs = df_grouped["legs"].mean()

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
unique_products = df_grouped["product"].nunique()

digest_cols = st.columns([1.4, 1])

with digest_cols[0]:
    st.markdown("#### Session digest")
    st.markdown(
        """
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:4px;">
            <div class="data-chip"><span class="data-chip__dot"></span>Rows: <strong>{rows}</strong></div>
            <div class="data-chip"><span class="data-chip__dot"></span>Products: <strong>{products}</strong></div>
            <div class="data-chip"><span class="data-chip__dot"></span>Period: <strong>{start} → {end}</strong></div>
        </div>
        """.format(
            rows=len(df_grouped),
            products=unique_products,
            start=date_start.strftime("%d %b %Y") if pd.notna(date_start) else "–",
            end=date_end.strftime("%d %b %Y") if pd.notna(date_end) else "–",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        - **Volume**: Keeps every ticket aggregated, no dilution between singles and combos.
        - **ROIs**: Rounded to 2 decimals for clinical readability.
        - **Markets**: Auto-bucketed by props, totals, lines and 1X2 where present.
        """
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


# ---------- TABS ----------
st.markdown("")
tab1, tab2, tab3 = st.tabs(["📊 Markets", "🎟 Tickets", "📄 Raw data"])

with tab1:
    st.markdown("#### Profitability by market group")
    if by_market_group is not None and not by_market_group.empty:
        num_cols_market = by_market_group.select_dtypes(include="number").columns
        formatter_market = {col: "{:.2f}" for col in num_cols_market}
        st.dataframe(
            by_market_group.style
                .applymap(color_roi, subset=["roi"])
                .format(formatter_market),
            use_container_width=True
        )
    else:
        st.info("No market data found in this file (missing 'market name').")

    if by_product is not None and not by_product.empty:
        st.markdown("#### ROI by product")
        product_chart_df = by_product.reset_index().rename(columns={"index": "product"})
        roi_bar = (
            alt.Chart(product_chart_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("product:N", sort="-y", title="Product"),
                y=alt.Y("roi:Q", title="ROI %"),
                color=alt.Color(
                    "roi:Q",
                    title="ROI %",
                    scale=alt.Scale(domainMid=0, scheme="tealred"),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("product:N", title="Product"),
                    alt.Tooltip("roi:Q", title="ROI %", format=".2f"),
                    alt.Tooltip("stake:Q", title="Stake", format=".2f"),
                    alt.Tooltip("ret:Q", title="Return", format=".2f"),
                ],
            )
            .properties(height=320)
        )

        roi_labels = (
            alt.Chart(product_chart_df)
            .mark_text(fontWeight="bold", dx=8, dy=-1, color="#e8edf4")
            .encode(
                x=alt.X("product:N", sort="-y"),
                y=alt.Y("roi:Q"),
                text=alt.Text("roi:Q", format="+.1f"),
                color=alt.condition("datum.roi >= 0", alt.value("#baf7e4"), alt.value("#ffb2b2")),
            )
        )

        zero_line = alt.Chart(product_chart_df).mark_rule(color="#263040", strokeDash=[4, 4]).encode(y=alt.datum(0))

        roi_chart = (
            (roi_bar + roi_labels + zero_line)
            .configure_axis(grid=False, labelColor="#e8edf4", titleColor="#e8edf4")
            .configure_view(strokeOpacity=0)
            .configure_legend(labelColor="#e8edf4", titleColor="#e8edf4")
        )

        st.altair_chart(roi_chart, use_container_width=True)

with tab2:
    st.markdown("#### Live vs Prematch")
    num_cols_prod = by_product.select_dtypes(include="number").columns
    formatter_prod = {col: "{:.2f}" for col in num_cols_prod}
    st.dataframe(
        by_product.style
            .applymap(color_roi, subset=["roi"])
            .format(formatter_prod),
        use_container_width=True
    )

    st.markdown("#### Combo vs Single")
    num_cols_ticket = by_ticket.select_dtypes(include="number").columns
    formatter_ticket = {col: "{:.2f}" for col in num_cols_ticket}
    st.dataframe(
        by_ticket.style
            .applymap(color_roi, subset=["roi"])
            .format(formatter_ticket),
        use_container_width=True
    )

with tab3:
    with st.expander("Ticket-level data (aggregated singles & combos)", expanded=True):
        num_cols_grouped = df_grouped.select_dtypes(include="number").columns
        formatter_grouped = {col: "{:.2f}" for col in num_cols_grouped}
        st.dataframe(
            df_grouped.style.format(formatter_grouped),
            use_container_width=True
        )
