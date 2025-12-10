import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="PlayWise Pilot", layout="wide")

pd.options.display.float_format = "{:.2f}".format

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
.main {
    background: radial-gradient(circle at top left, #1c2833 0, #05070b 45%, #020308 100%);
}
[data-testid="stSidebar"] {
    background: #05070b;
    border-right: 1px solid #1f2933;
}
[data-testid="stSidebar"] h2 {
    font-weight: 800 !important;
    letter-spacing: 0.08em;
    font-size: 1.1rem !important;
}
h1 {
    font-weight: 800 !important;
    font-size: 2.4rem !important;
    letter-spacing: 0.04em;
    margin-bottom: 0.25rem;
}
.playwise-subtitle {
    font-size: 0.95rem;
    opacity: 0.75;
    margin-bottom: 0.5rem;
}
.hero-card {
    background: rgba(9, 12, 20, 0.9);
    border-radius: 18px;
    padding: 20px 22px 18px 22px;
    border: 1px solid #202632;
    box-shadow: 0 18px 50px rgba(0,0,0,0.55);
}
.element-container:has(div[data-testid="metric-container"]) {
    background: #080b11;
    border-radius: 14px;
    padding: 14px 14px 10px 14px;
    border: 1px solid #222833;
    box-shadow: 0 4px 14px rgba(0,0,0,0.55);
    transition: all 0.12s ease;
}
.element-container:has(div[data-testid="metric-container"]):hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.7);
}
.stTabs [role="tab"] {
    padding: 10px 22px;
    font-size: 0.95rem;
    font-weight: 600;
}
.stTabs [role="tab"][aria-selected="true"] {
    border-bottom: 3px solid #38ef7d;
}
div[data-testid="dataframe"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #222733;
    margin-top: 10px;
}
.stExpander {
    border-radius: 12px !important;
    border: 1px solid #222733 !important;
    background: rgba(7,10,16,0.8) !important;
}
h3, h4 {
    font-weight: 700 !important;
}
.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: rgba(56, 239, 125, 0.09);
    color: #96f7c4;
    border: 1px solid rgba(56,239,125,0.4);
    margin-bottom: 6px;
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
st.markdown('<p class="playwise-subtitle">Your stats. Your edge.</p>', unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="section-pill">SETUP</div>
            <h3 style="margin-top:2px;">Upload your first betting history</h3>
            <p style="opacity:0.8; font-size:0.9rem; max-width:460px;">
                Drop in a Sportsbook Excel export in the sidebar and PlayWise will turn it
                into a clean overview of your betting performance: ROI, profit, market edges
                and your betting profile.
            </p>
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
