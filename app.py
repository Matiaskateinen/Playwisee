import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from imports.coolbet import NormalizationError, normalize_coolbet_data
from imports.unibet_paste import normalize_unibet_paste, parse_unibet_paste
from imports.ui import (
    inject_global_css,
    open_page_wrap,
    close_page_wrap,
    render_sidebar_loader,
    render_hero,
    spacer,
)

st.set_page_config(page_title="PlayWise Pilot", layout="wide")

# Shared helpers -------------------------------------------------------------
def parse_unibet_into_session(raw_text: str, button_key: str) -> None:
    """Parse Unibet freeform paste content and store it into session state."""

    if st.button("Parse Unibet paste", key=button_key):
        bets_df, legs_df = parse_unibet_paste(raw_text)
        st.markdown("**Parsed bets (Unibet)**")
        st.dataframe(bets_df)
        st.markdown("**Parsed legs (Unibet)**")
        st.dataframe(legs_df)
        normalized_unibet = normalize_unibet_paste(raw_text)
        st.session_state["parsed_unibet_df"] = normalized_unibet


# Initialize session state slot for Unibet pastes to avoid NameError in downstream checks
if "unibet_df" not in st.session_state:
    st.session_state["unibet_df"] = None

if "parsed_unibet_df" not in st.session_state:
    st.session_state["parsed_unibet_df"] = None

# Always-available data entry in sidebar so uploads are reachable after first load
with st.sidebar:
    sidebar_upload = render_sidebar_loader(parse_unibet_into_session)

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
inject_global_css()

open_page_wrap()

parsed_unibet_df = st.session_state.get("parsed_unibet_df")
show_hero = (sidebar_upload is None) and (parsed_unibet_df is None)

if show_hero:
    hero_upload = render_hero(parse_unibet_into_session)
    uploaded_file = sidebar_upload or hero_upload
    close_page_wrap()
    spacer()
else:
    uploaded_file = sidebar_upload
    close_page_wrap()
    spacer()

parsed_unibet_df = st.session_state.get("parsed_unibet_df")

if uploaded_file is None and parsed_unibet_df is None:
    st.stop()

# ---------- DATA PROCESSING ----------
if parsed_unibet_df is not None:
    df = parsed_unibet_df
else:
    df_raw = safe_read_excel(uploaded_file)
    try:
        df = normalize_coolbet_data(df_raw)
    except NormalizationError as exc:  # pragma: no cover - streamlit surface
        st.error(str(exc))
        st.stop()

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

legs_agg = ("legs", "max") if "legs" in df.columns else ("odds", "size")
df_grouped = (
    df.groupby(["date", "rank", "ticket type", "product"], as_index=False)
      .agg(
          bets=("bets", "sum"),
          wins=("wins", "sum"),
          total_odds=("odds", np.prod),
          legs=legs_agg
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

# ---------- NAVIGATION ----------
nav_choice = st.sidebar.radio(
    "Navigate",
    ["Profile", "Deep Dives", "Markets/Tickets"],
    index=0,
    help="Jump between your profile, deep dives, and market/ticket breakdowns.",
)

def color_roi(v):
    if pd.isna(v): return ""
    return "color: green" if v > 0 else "color: red" if v < 0 else "color: gray"


# ---------- HERO OVERVIEW CARD ----------

st.markdown('<div class="section-pill">TIMELINE</div>', unsafe_allow_html=True)
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
    selected_range = st.selectbox(
        "Timeline range",
        list(range_options.keys()),
        index=default_range,
        label_visibility="collapsed",
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
        st.write(
            f"📈 Strongest edge in **{str(best).title()}** "
            f"({by_market_group.loc[best, 'roi']:.2f}%)."
        )
        losing = by_market_group[by_market_group["roi"] < 0]
        if not losing.empty:
            worst = by_market_group["roi"].idxmin()
            st.write(
                f"📉 Weakest in **{str(worst).title()}** "
                f"({by_market_group.loc[worst, 'roi']:.2f}%)."
            )
    else:
        st.write("ℹ️ Add more bets to unlock market insights.")

    if total_stake > 0:
        st.write(f"💶 Total volume tracked: **{total_stake:.2f} €**")

st.markdown('</div>', unsafe_allow_html=True)  # end hero-card


# ---------- QUICK DIGEST / PROFILE ----------
if nav_choice == "Profile":
    date_start = df_filtered["date"].min()
    date_end = df_filtered["date"].max()
    win_rate = round((df_filtered["wins"] > 0).mean() * 100, 1)
    loss_rate = round(100 - win_rate, 1)
    total_bets_count = len(df_filtered_raw)
    singles_share = (num_singles / total_bets_count * 100) if total_bets_count else 0
    combos_share = (num_combos / total_bets_count * 100) if total_bets_count else 0
    time_span = "–"
    if pd.notna(date_start) and pd.notna(date_end):
        time_span = f"{date_start.strftime('%b %Y')} – {date_end.strftime('%b %Y')}"

    roi_class = "stat-value stat-value--pos" if roi_total >= 0 else "stat-value stat-value--neg"
    pl_class = "stat-value stat-value--pos" if total_profit >= 0 else "stat-value stat-value--neg"

    st.markdown(
        """
        <div class="profile-header">
            <div>
                <h3 class="profile-title">Profile</h3>
                <p class="profile-subtitle">Your betting style at a glance</p>
            </div>
            <div class="profile-chip">{time_span}</div>
        </div>
        """.format(time_span=time_span),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="profile-card profile-card--wide">
            <div class="profile-card__header">
                <div>
                    <div class="eyebrow">Profile Summary</div>
                    <h4 class="profile-card__title">Stats overview</h4>
                </div>
                <div class="mini-chip">{total_bets_count} bets</div>
            </div>
            <div class="profile-main-grid">
                <div class="profile-stats">
                    <div class="stat-grid">
                        <div class="stat-item">
                            <span class="stat-label">ROI</span>
                            <div class="{roi_class}">{roi_total:.2f}%</div>
                            <div class="stat-help">Return across all tracked stakes</div>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Net P/L</span>
                            <div class="{pl_class}">{total_profit:.2f} €</div>
                            <div class="stat-help">Total profit/loss to date</div>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Avg stake</span>
                            <div class="stat-value">{avg_bet:.2f} €</div>
                            <div class="stat-help">Mean stake per ticket</div>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Total bets</span>
                            <div class="stat-value">{total_bets_count}</div>
                            <div class="stat-help">Tickets tracked in this span</div>
                        </div>
                    </div>
                    <div class="profile-bars">
                        <div class="bar-row">
                            <div class="bar-label">Singles vs Combos</div>
                            <div class="bar-track">
                                <span class="bar-fill bar-fill--primary" style="width:{singles_share:.1f}%;"></span>
                                <span class="bar-fill bar-fill--secondary" style="width:{combos_share:.1f}%;"></span>
                            </div>
                            <div class="bar-legend">
                                <span>Singles {num_singles}</span>
                                <span>Combos {num_combos}</span>
                            </div>
                        </div>
                        <div class="bar-row">
                            <div class="bar-label">Win / Loss</div>
                            <div class="bar-track">
                                <span class="bar-fill bar-fill--primary" style="width:{win_rate:.1f}%;"></span>
                                <span class="bar-fill bar-fill--negative" style="width:{loss_rate:.1f}%;"></span>
                            </div>
                            <div class="bar-legend">
                                <span>Win {win_rate:.1f}%</span>
                                <span>Loss {loss_rate:.1f}%</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="profile-rings">
                    <div class="ring-card">
                        <div class="ring" style="--percent:{win_rate};">
                            <div class="ring__center">
                                <div class="ring__value">{win_rate:.0f}%</div>
                                <div class="ring__label">Win rate</div>
                            </div>
                        </div>
                        <div class="ring-foot">Solid momentum</div>
                    </div>
                    <div class="ring-card">
                        <div class="ring ring--accent" style="--percent:{max(min(roi_total,100),0)};">
                            <div class="ring__center">
                                <div class="ring__value">{roi_total:.0f}%</div>
                                <div class="ring__label">ROI</div>
                            </div>
                        </div>
                        <div class="ring-foot">Return efficiency</div>
                    </div>
                </div>
            </div>
        </div>
        """.format(
            roi_class=roi_class,
            pl_class=pl_class,
            roi_total=roi_total,
            total_profit=total_profit,
            avg_bet=avg_bet,
            total_bets_count=total_bets_count,
            win_rate=win_rate,
            num_singles=num_singles,
            num_combos=num_combos,
            time_span=time_span,
            singles_share=singles_share,
            combos_share=combos_share,
            loss_rate=loss_rate,
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card-row">
            <div class="profile-card">
                <h4 style="margin:4px 0 12px 0;">Session digest</h4>
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
            </div>
            <div class="profile-card">
                <h4 style="margin:4px 0 12px 0;">Session notes</h4>
                <ul style="margin: 0; padding-left: 18px; color: var(--text);">
                    <li>Mean stake per ticket: <strong>{avg_bet:.2f} €</strong></li>
                </ul>
            </div>
        </div>
        """.format(
            rows=len(df_filtered),
            start=date_start.strftime("%d %b %Y") if pd.notna(date_start) else "–",
            end=date_end.strftime("%d %b %Y") if pd.notna(date_end) else "–",
            win=win_rate,
            loss=loss_rate,
            avg_bet=avg_bet,
        ),
        unsafe_allow_html=True,
    )


# ---------- INTERACTIVE SECTIONS ----------

if nav_choice == "Deep Dives":
    st.markdown("### Deep dives")
    st.markdown("#### Micro-highlights")
    if by_product is not None and not by_product.empty:
        best_product = by_product["roi"].idxmax()
        st.write(
            f"✅ Strongest lane: **{str(best_product).title()}** "
            f"({by_product.loc[best_product, 'roi']:.2f}% ROI)"
        )
        worst_product = by_product["roi"].idxmin()
        st.write(
            f"⚠️ Watchlist: **{str(worst_product).title()}** "
            f"({by_product.loc[worst_product, 'roi']:.2f}% ROI)"
        )
    st.write(f"🧮 Mean stake per ticket: **{avg_bet:.2f} €**")
    st.markdown("<div class='section-stack'>", unsafe_allow_html=True)
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    with st.expander("📊 Markets — click to open full view", expanded=False):
        st.markdown("#### Profitability By Market Group")
        if by_market_group is not None and not by_market_group.empty:
            display_by_market = by_market_group.copy()
            display_by_market.index = display_by_market.index.map(lambda x: str(x).title())
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
        display_by_product.index = display_by_product.index.map(lambda x: str(x).title())
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
        display_by_ticket.index = display_by_ticket.index.map(lambda x: str(x).title())
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

    st.markdown("</div>", unsafe_allow_html=True)

if nav_choice == "Markets/Tickets":
    st.markdown("### Markets & Tickets")
    st.markdown("<div class='section-stack'>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    with st.expander("📊 Markets — click to open full view", expanded=True):
        st.markdown("#### Profitability By Market Group")
        if by_market_group is not None and not by_market_group.empty:
            display_by_market = by_market_group.copy()
            display_by_market.index = display_by_market.index.map(lambda x: str(x).title())
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
    with st.expander("🎟 Tickets — click to open full view", expanded=True):
        st.markdown("#### Live Vs Prematch")
        display_by_product = by_product.copy()
        display_by_product.index = display_by_product.index.map(lambda x: str(x).title())
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
        display_by_ticket.index = display_by_ticket.index.map(lambda x: str(x).title())
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
        for col in display_grouped.select_dtypes(include="object").columns:
            display_grouped[col] = display_grouped[col].astype(str).str.title()
        num_cols_grouped = display_grouped.select_dtypes(include="number").columns
        formatter_grouped = {col: "{:.2f}" for col in num_cols_grouped}
        st.dataframe(
            display_grouped.style.format(formatter_grouped),
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
