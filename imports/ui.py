import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
<style>
:root {
    --bg: #060910;
    --card: #0b101a;
    --stroke: #1c2635;
    --muted: #9fb2c7;
    --text: #eef2f7;
    --accent: #46e3c4;
    --glow-blue: rgba(0, 157, 255, 0.1);
    --glow-green: rgba(65, 240, 192, 0.14);
}
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
    background: var(--bg);
    letter-spacing: 0.01em;
}
.app-wrapper {
    position: relative;
    isolation: isolate;
}
.main {
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at 20% 20%, rgba(65, 240, 192, 0.06), transparent 26%),
                radial-gradient(circle at 82% 4%, rgba(0, 157, 255, 0.06), transparent 24%),
                linear-gradient(135deg, #060910 0%, #070b13 50%, #05070d 100%);
}
.main:before {
    content: '';
    position: fixed;
    inset: -28% -18% 24% -18%;
    background-image: linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
    background-size: 78px 78px;
    opacity: 0.18;
    pointer-events: none;
    z-index: 0;
    transform: perspective(1100px) rotateX(70deg) rotateZ(8deg) translate3d(-4%, -6%, 0);
    animation: gridDrift 42s ease-in-out infinite alternate;
}
.main:after {
    content: '';
    position: fixed;
    inset: -8% -26% auto -26%;
    height: 76vh;
    background:
        radial-gradient(closest-side at 28% 38%, var(--glow-green), transparent 65%),
        radial-gradient(closest-side at 72% 58%, var(--glow-blue), transparent 60%),
        radial-gradient(closest-side at 46% 80%, rgba(255, 255, 255, 0.05), transparent 60%);
    filter: blur(10px);
    mix-blend-mode: screen;
    opacity: 0.4;
    pointer-events: none;
    z-index: 0;
    transform: perspective(1400px) rotateX(66deg) rotateZ(-4deg) translate3d(0, -6%, 0);
    animation: warpGlow 48s ease-in-out infinite alternate;
}
@keyframes gridDrift {
    0% {
        transform: perspective(1100px) rotateX(70deg) rotateZ(8deg) translate3d(-4%, -6%, 0);
    }
    100% {
        transform: perspective(1100px) rotateX(67deg) rotateZ(4deg) translate3d(3%, -4%, 0);
    }
}
@keyframes warpGlow {
    0% {
        transform: perspective(1400px) rotateX(66deg) rotateZ(-4deg) translate3d(0, -6%, 0);
    }
    100% {
        transform: perspective(1400px) rotateX(64deg) rotateZ(0deg) translate3d(-2%, -8%, 0);
    }
}

/* Surface system */
.pw-surface {
    position: relative;
    background: linear-gradient(160deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
    transition: border-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
    overflow: hidden;
}
.hero-card,
.upload-card,
.section-card,
.element-container:has(div[data-testid="metric-container"]),
div[data-testid="dataframe"] {
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    box-shadow: 0 18px 48px rgba(0,0,0,0.42);
}
.pw-surface--focus {
    border-color: rgba(70, 227, 196, 0.4);
    box-shadow: 0 22px 60px rgba(0,0,0,0.48), 0 1px 0 rgba(255,255,255,0.04);
}
.pw-surface--plain {
    box-shadow: none;
    border-color: rgba(255,255,255,0.05);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11,16,26,0.96), rgba(6,9,15,0.98));
    border-right: 1px solid var(--stroke);
    box-shadow: 6px 0 26px rgba(0,0,0,0.35);
    padding-top: 14px;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-weight: 800 !important;
    letter-spacing: 0.06em;
    font-size: 1.04rem !important;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
[data-testid="stSidebar"] .st-emotion-cache-1q7ch1g p {
    color: var(--muted);
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    display: block;
    padding: 10px 12px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    background: rgba(255,255,255,0.02);
    transition: border-color 0.16s ease, background 0.16s ease, transform 0.16s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: rgba(70, 227, 196, 0.5);
    background: rgba(70, 227, 196, 0.06);
}
[data-testid="stSidebar"] [role="radiogroup"] label[aria-checked="true"] {
    border-color: rgba(70, 227, 196, 0.8);
    background: linear-gradient(135deg, rgba(70, 227, 196, 0.12), rgba(0, 157, 255, 0.08));
    transform: translateY(-1px);
}

h1 {
    font-weight: 800 !important;
    font-size: 2.4rem !important;
    letter-spacing: 0.02em;
    margin-bottom: 0.25rem;
}
h2 {
    font-weight: 800 !important;
    letter-spacing: 0.01em;
}
h3, h4 {
    font-weight: 700 !important;
    letter-spacing: 0.01em;
}

.page-wrap {
    max-width: 1180px;
    margin: 0 auto;
    padding: 24px 18px 0 18px;
}

.nav-link-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    margin: 8px 0;
    border: 1px solid var(--stroke);
    border-radius: 14px;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.08), rgba(0, 157, 255, 0.08));
    color: var(--text);
    text-decoration: none;
    font-weight: 600;
    transition: transform 0.12s ease, border-color 0.12s ease, box-shadow 0.12s ease;
}
.nav-link-btn:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.nav-link-btn .chevron {
    margin-left: auto;
    color: var(--accent);
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
    position: fixed;
    top: 18px;
    left: 18px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.14), rgba(0, 167, 255, 0.14));
    color: #b1f4df;
    border: 1px solid rgba(65, 240, 192, 0.35);
    z-index: 9999;
}
.playwise-subtitle {
    font-size: 1rem;
    color: var(--muted);
    margin-bottom: 0.8rem;
    letter-spacing: 0.01em;
}
.hero-headline {
    font-size: 1.5rem;
    margin-bottom: 0.4rem;
    font-weight: 750;
}
.hero-description {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.7;
    max-width: 640px;
    margin-bottom: 0.7rem;
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
    line-height: 1.5;
}
.hero-bullets li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--accent);
    opacity: 0.9;
}

.upload-card {
    position: relative;
    background: linear-gradient(160deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)), var(--card);
    border-radius: 18px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 18px 46px rgba(0,0,0,0.42);
}
.upload-card__inner {
    background: rgba(255,255,255,0.02);
    border-radius: 14px;
    padding: 12px 14px 10px 14px;
    border: 1px solid rgba(255,255,255,0.05);
}
.upload-card__title {
    font-weight: 800;
    letter-spacing: 0.03em;
    margin-bottom: 6px;
}
.upload-card__helper {
    margin: 0 0 8px 0;
    color: var(--muted);
    font-size: 0.94rem;
}
.hero-spacer {
    height: 32px;
}

.hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border-radius: 18px;
    padding: 24px 26px 22px 26px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
}
.hero-card:before,
.hero-card:after {
    content: '';
    position: absolute;
    border-radius: 24px;
    filter: blur(10px);
    opacity: 0.5;
}
.hero-card:before {
    inset: -12% auto auto -10%;
    width: 34%;
    height: 36%;
    background: radial-gradient(circle, rgba(65, 240, 192, 0.12), transparent 60%);
}
.hero-card:after {
    inset: auto -26% -24% auto;
    width: 30%;
    height: 32%;
    background: radial-gradient(circle, rgba(0, 167, 255, 0.12), transparent 55%);
}

.hero-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-top: 16px;
    position: relative;
    z-index: 1;
}
.hero-grid__item {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 12px 14px;
}
.hero-label {
    display: block;
    font-size: 0.76rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
}
.hero-value {
    font-weight: 750;
    color: var(--text);
    font-size: 1.05rem;
}

.element-container:has(div[data-testid="metric-container"]) {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border-radius: 18px;
    padding: 16px 16px 12px 16px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 16px 40px rgba(0,0,0,0.4);
    transition: all 0.12s ease;
}
.element-container:has(div[data-testid="metric-container"]):hover {
    transform: translateY(-2px);
    border-color: rgba(70, 227, 196, 0.55);
    box-shadow: 0 18px 48px rgba(0,0,0,0.42);
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    letter-spacing: 0.02em;
    font-size: 0.88rem !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 800 !important;
    font-size: 1.6rem !important;
    line-height: 1.2 !important;
}

.section-stack {
    display: grid;
    gap: 18px;
    margin-top: 12px;
}

.section-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 16px 16px 12px 16px;
    box-shadow: 0 18px 48px rgba(0,0,0,0.42);
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
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
    margin-top: 12px;
    background: rgba(11, 16, 26, 0.92);
    box-shadow: 0 12px 32px rgba(0,0,0,0.35);
}
.stDataFrame table {
    border-spacing: 0;
    width: 100%;
}
.stDataFrame thead tr {
    background: rgba(255,255,255,0.04);
    color: var(--text);
    font-weight: 700;
}
.stDataFrame th,
.stDataFrame td {
    padding: 12px 14px !important;
    border: none !important;
}
.stDataFrame tbody tr:nth-child(odd) { background: rgba(255,255,255,0.01); }
.stDataFrame tbody tr:nth-child(even) { background: rgba(255,255,255,0.03); }
.stDataFrame tbody tr:hover { background: rgba(70, 227, 196, 0.08); }

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
    background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 14px 16px 12px 16px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.4);
}
.digest-label {
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
}
.digest-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 8px;
}
.digest-value .win { color: var(--accent); }
.digest-value .loss { color: #ff8b8b; }

.stExpander {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(7,10,16,0.85) !important;
}

.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 18px;
    border-radius: 999px;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.12), rgba(0, 167, 255, 0.12));
    color: #b1f4df;
    border: 1px solid rgba(65, 240, 192, 0.35);
    margin-bottom: 8px;
}

.stFileUploader div[data-testid="stFileUploaderDropzone"] {
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 10px;
    transition: border-color 0.16s ease, background 0.16s ease;
}
.stFileUploader div[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(70, 227, 196, 0.65);
    background: rgba(70, 227, 196, 0.06);
}
.stat-label {
    display: block;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.stat-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.2;
}
.stat-value--pos { color: #8af2d9; }
.stat-value--neg { color: #ff9c9c; }
.stat-help {
    margin-top: 2px;
    color: var(--muted);
    font-size: 0.9rem;
}
.card-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
    margin-top: 12px;
}
.stat-label {
    display: block;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.stat-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.2;
}
.stat-value--pos { color: #8af2d9; }
.stat-value--neg { color: #ff9c9c; }
.stat-help {
    margin-top: 2px;
    color: var(--muted);
    font-size: 0.9rem;
}
.card-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
    margin-top: 12px;
}
.stat-label {
    display: block;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.stat-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.2;
}
.stat-value--pos { color: #8af2d9; }
.stat-value--neg { color: #ff9c9c; }
.stat-help {
    margin-top: 2px;
    color: var(--muted);
    font-size: 0.9rem;
}
.profile-bars {
    display: grid;
    gap: 10px;
    margin-top: 6px;
}
.bar-row {
    display: grid;
    gap: 6px;
}
.bar-label {
    color: var(--muted);
    font-size: 0.85rem;
    letter-spacing: 0.04em;
}
.bar-track {
    position: relative;
    display: flex;
    width: 100%;
    height: 12px;
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.bar-fill {
    height: 100%;
    display: block;
}
.bar-fill--primary { background: linear-gradient(90deg, #6cf0d6, #58e2c9); }
.bar-fill--secondary { background: linear-gradient(90deg, #8694ff, #b19cff); }
.bar-fill--negative { background: linear-gradient(90deg, #ff9898, #ff7f7f); }
.bar-legend {
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 0.88rem;
}
.profile-rings {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
}
.ring-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    display: grid;
    gap: 8px;
}
.ring {
    --size: 140px;
    width: var(--size);
    height: var(--size);
    border-radius: 50%;
    background: conic-gradient(#58e2c9 calc(var(--percent) * 1%), rgba(255,255,255,0.08) 0);
    display: grid;
    place-items: center;
    margin: 0 auto;
    border: 10px solid rgba(255,255,255,0.03);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
}
.ring--accent {
    background: conic-gradient(#8ab9ff calc(var(--percent) * 1%), rgba(255,255,255,0.08) 0);
}
.ring__center {
    background: rgba(0,0,0,0.35);
    border-radius: 50%;
    width: 70%;
    height: 70%;
    display: grid;
    place-items: center;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 6px 16px rgba(0,0,0,0.35);
}
.ring__value {
    font-size: 1.4rem;
    font-weight: 800;
}
.ring__label {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.ring-foot {
    color: var(--muted);
    font-size: 0.9rem;
}
.card-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
    margin-top: 12px;
}
</style>
""",
        unsafe_allow_html=True,
    )


def open_page_wrap() -> None:
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)


def close_page_wrap() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def spacer(height: int = 32) -> None:
    if height == 32:
        st.markdown("<div class='hero-spacer'></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='height:{height}px'></div>", unsafe_allow_html=True)


def render_sidebar_loader(parse_unibet_callback):
    st.markdown("#### Load data")
    uploaded_file = st.file_uploader("Upload Sportsbook Excel", type=["xlsx"], key="sidebar_excel")
    st.caption("Tip: export your betting history as .xlsx and drop it here.")
    with st.expander("Or paste Unibet bet history", expanded=False):
        raw_text_sidebar = st.text_area("Paste your Unibet bet history here", height=180, key="sidebar_unibet")
        parse_unibet_callback(raw_text_sidebar, "parse_unibet_paste_sidebar")
    return uploaded_file


def render_hero(parse_unibet_callback):
    hero_cols = st.columns([1.05, 0.95])

    with hero_cols[0]:
        st.markdown(
            """
            <div class="hero-copy">
                <div class="hero-pill">PlayWise · 1.022 </div>
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
        uploaded_file_hero = st.file_uploader("", type=["xlsx"], key="hero_excel")
        st.caption("Tip: export your betting history as .xlsx and drop it here.")
        with st.expander("Or paste Unibet bet history", expanded=False):
            raw_text = st.text_area("Paste your Unibet bet history here", height=200, key="hero_unibet")
            parse_unibet_callback(raw_text, "parse_unibet_paste")
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    return uploaded_file_hero
