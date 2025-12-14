"""Thin wrapper module to avoid circular imports when using UI helpers."""

from .ui_helpers import (
    inject_global_css,
    open_page_wrap,
    close_page_wrap,
    render_sidebar_loader,
    render_hero,
    spacer,
)

PROFILE_CSS = """
<style>
.pw-profile-wrap {
    max-width: 1180px;
    margin: 0 auto;
    display: grid;
    gap: 18px;
    padding: 0 8px 18px;
}
.pw-profile-header {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px 20px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.38);
}
.pw-profile-header__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
}
.pw-profile-header__left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.pw-avatar {
    width: 66px;
    height: 66px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
    display: grid;
    place-items: center;
    box-shadow: 0 10px 26px rgba(0,0,0,0.4);
}
.pw-avatar__inner {
    width: 88%;
    height: 88%;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, rgba(70, 227, 196, 0.14), rgba(0, 157, 255, 0.14));
    color: #c9f8ec;
    font-weight: 800;
    letter-spacing: 0.08em;
}
.pw-profile-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin: 0;
}
.pw-profile-subtitle {
    color: var(--muted);
    margin: 2px 0 0 0;
}
.pw-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text);
    font-weight: 600;
}
.pw-mini-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    align-items: stretch;
    min-width: 260px;
}
.pw-mini-stat {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 10px 12px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}
.pw-stats-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0)), var(--card);
    border: 1px solid var(--stroke);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.36);
}
.pw-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 10px;
}
.pw-stat {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 12px;
    display: grid;
    gap: 4px;
}
.pw-stat__label {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
}
.pw-stat__value {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.2;
}
.pw-stat__help {
    font-size: 0.92rem;
    color: var(--muted);
}
.is-pos { color: #8af2d9; }
.is-neg { color: #ff9c9c; }
.pw-two-col {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
}
</style>
"""

__all__ = [
    "inject_global_css",
    "open_page_wrap",
    "close_page_wrap",
    "render_sidebar_loader",
    "render_hero",
    "spacer",
    "PROFILE_CSS",
]
