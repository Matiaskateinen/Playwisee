import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
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
.nav-link-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    margin: 8px 0;
    border: 1px solid var(--stroke);
    border-radius: 12px;
    background: linear-gradient(120deg, rgba(65, 240, 192, 0.08), rgba(0, 157, 255, 0.08));
    color: var(--text);
    text-decoration: none;
    font-weight: 600;
    transition: transform 0.12s ease, border-color 0.12s ease;
}
.nav-link-btn:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
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

    background: linear-gradient(120deg, rgba(65, 240, 192, 0.18), rgba(0, 167, 255, 0.18));
    color: #9bf6da;
    border: 1px solid rgba(65, 240, 192, 0.45);
    z-index: 9999; /* Always on top */
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
    padding: 10px 18px;
    border-radius: 999px;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
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
