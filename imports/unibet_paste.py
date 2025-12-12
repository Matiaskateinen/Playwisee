"""Parse and normalize Unibet bet history pasted as raw text.

This module mirrors the output schema of :mod:`imports.coolbet` so the
Streamlit dashboard can render graphs from Unibet pastes the same way it does
for Coolbet Excel uploads.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

import pandas as pd

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

DATE_PATTERN = re.compile(r"(\d{2}\.\d{2}\.\d{4})\s*klo\s*[•.]?\s*(\d{2}\.\d{2}\.\d{2})")
COUPON_PATTERN = re.compile(r"Kuponkitunnus:\s*(\d+)", re.IGNORECASE)
HEADER_PATTERN = re.compile(r"^(Single|Tupla|Tripla|Parlay|Tuplavoitettu)", re.IGNORECASE)
STATUS_PATTERN = re.compile(r"(Voitettu|Vireill[aä]|H[aä]vitty|Peruttu)", re.IGNORECASE)


@dataclass
class ParsedBet:
    bet_id: str | None
    placed_at: pd.Timestamp | None
    bet_type: str | None
    status: str | None
    stake: float | None
    odds: float | None
    payout: float | None
    legs: List[dict]


def _normalize_number(value: str | None) -> float | None:
    if not value:
        return None

    cleaned = value.replace("€", "").replace(" ", "")
    cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def _parse_datetime(text: str) -> pd.Timestamp | None:
    match = DATE_PATTERN.search(text)
    if not match:
        return None

    date_part, time_part = match.groups()
    time_part = time_part.replace(".", ":")
    try:
        dt = datetime.strptime(f"{date_part} {time_part}", "%d.%m.%Y %H:%M:%S")
    except ValueError:
        return None

    return pd.Timestamp(dt, tz="UTC")


def _split_sections(raw_text: str) -> List[str]:
    """Split the pasted blob into bet sections.

    Unibet pastes sometimes start with a ticket summary (e.g. ``TuplaVoitettu``)
    followed by the actual coupon row. We treat both the summary header and the
    ``Kuponkitunnus`` line as boundaries so each section stays intact.
    """

    sections: List[str] = []
    current: List[str] = []
    pending_header: List[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if COUPON_PATTERN.match(line):
            if current:
                sections.append("\n".join(current).strip())
            current = pending_header + [line]
            pending_header = []
            continue

        if HEADER_PATTERN.match(line):
            if current:
                sections.append("\n".join(current).strip())
                current = []
            pending_header = [line]
            continue

        if pending_header and not current:
            pending_header.append(line)
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())
    elif pending_header:
        sections.append("\n".join(pending_header).strip())

    return [s for s in sections if s]


def _parse_legs(lines: List[str], bet_id: str | None, overall_odds: float | None) -> List[dict]:
    legs: List[dict] = []

    leg_pattern = re.compile(r"(.+?)@\s*([0-9.,]+)")
    for idx, line in enumerate(lines):
        match = leg_pattern.search(line)
        if not match:
            continue

        left, odds_text = match.groups()
        odds = _normalize_number(odds_text)

        if ":" in left:
            market, selection = [part.strip() for part in left.split(":", 1)]
        else:
            market, selection = None, left.strip()

        event = None
        for follow in lines[idx + 1 : idx + 3]:
            if " - " in follow:
                event = follow.strip()
                break

        legs.append(
            {
                "bet_id": bet_id,
                "event": event,
                "market": market or None,
                "selection": selection or None,
                "odds": odds,
            }
        )

    if not legs:
        # Fallback to a single leg using the overall odds
        legs.append(
            {
                "bet_id": bet_id,
                "event": next((ln for ln in lines if " - " in ln), None),
                "market": None,
                "selection": None,
                "odds": overall_odds,
            }
        )

    return legs


def _parse_section(section: str) -> ParsedBet:
    lines = [ln.strip() for ln in section.splitlines() if ln.strip()]
    text_blob = "\n".join(lines)

    bet_id_match = COUPON_PATTERN.search(text_blob)
    bet_id = bet_id_match.group(1) if bet_id_match else None

    placed_at = _parse_datetime(text_blob)

    bet_type_match = HEADER_PATTERN.search(lines[0]) if lines else None
    bet_type = bet_type_match.group(1).capitalize() if bet_type_match else None
    if bet_type and bet_type.lower().startswith("tupla"):
        bet_type = "Tupla"

    status_match = STATUS_PATTERN.search(text_blob)
    status = status_match.group(1).capitalize() if status_match else None

    stake_match = re.search(r"Panos:\s*€?([0-9.,]+)", text_blob)
    stake = _normalize_number(stake_match.group(1)) if stake_match else None

    payout_match = re.search(r"Voitto:\s*€?([0-9.,]+)", text_blob)
    payout = _normalize_number(payout_match.group(1)) if payout_match else None

    odds_match = re.search(r"Kertoimet:\s*([0-9.,]+)", text_blob)
    if not odds_match:
        odds_match = re.search(r"@\s*([0-9.,]+)", text_blob)
    odds = _normalize_number(odds_match.group(1)) if odds_match else None

    legs = _parse_legs(lines, bet_id, odds)

    return ParsedBet(
        bet_id=bet_id,
        placed_at=placed_at,
        bet_type=bet_type,
        status=status,
        stake=stake,
        odds=odds,
        payout=payout,
        legs=legs,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_unibet_paste(raw_text: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Parse Unibet bet history pasted as raw text.

    Returns two dataframes: ``bets`` (one per coupon) and ``legs`` (one per
    selection). These frames are intentionally minimal so they can be converted
    to the canonical Coolbet-like schema with :func:`normalize_unibet_paste`.
    """

    cleaned = raw_text.replace("\r\n", "\n")
    cleaned = re.sub(r"(\d),(?=\d{1,2}\b)", r"\1.", cleaned)

    sections = _split_sections(cleaned)
    parsed_bets = [_parse_section(section) for section in sections]

    bets_df = pd.DataFrame(
        [
            {
                "bet_id": bet.bet_id,
                "bookmaker": "Unibet",
                "placed_at": bet.placed_at,
                "bet_type": bet.bet_type,
                "stake": bet.stake,
                "odds": bet.odds,
                "payout": bet.payout,
                "status": bet.status,
                "leg_count": len(bet.legs),
            }
            for bet in parsed_bets
        ]
    )

    all_legs = [leg for bet in parsed_bets for leg in bet.legs]
    legs_df = pd.DataFrame(all_legs, columns=["bet_id", "event", "market", "selection", "odds"])

    if not bets_df.empty:
        bets_df["placed_at"] = pd.to_datetime(bets_df["placed_at"], utc=True, errors="coerce")

    return bets_df, legs_df


def normalize_unibet_paste(raw_text: str) -> pd.DataFrame:
    """Normalize a pasted Unibet history block to the Coolbet schema."""

    bets_df, legs_df = parse_unibet_paste(raw_text)

    status_map = {
        "voitettu": "won",
        "vireillä": "pending",
        "hävitty": "lost",
        "peruttu": "void",
    }

    type_map = {
        "single": "single",
        "tupla": "double",
        "tripla": "triple",
        "parlay": "parlay",
    }

    market_lookup = {}
    if not legs_df.empty:
        legs_df = legs_df.copy()
        legs_df["market"] = legs_df["market"].fillna(legs_df["selection"])
        for _, row in legs_df.iterrows():
            if row["bet_id"] not in market_lookup and pd.notna(row["market"]):
                market_lookup[row["bet_id"]] = row["market"]

    normalized_rows = []
    for _, bet in bets_df.iterrows():
        ticket_type = str(bet.get("bet_type", "")).strip().lower()
        ticket_type = type_map.get(ticket_type, ticket_type or "single")

        status_value = str(bet.get("status", "")).strip().lower()
        rank = status_map.get(status_value, status_value or "unknown")

        normalized_rows.append(
            {
                "date": pd.to_datetime(bet.get("placed_at"), utc=True, errors="coerce"),
                "rank": rank,
                "ticket type": ticket_type,
                "product": "unibet",
                "bets": pd.to_numeric(bet.get("stake"), errors="coerce"),
                "wins": pd.to_numeric(bet.get("payout"), errors="coerce"),
                "odds": pd.to_numeric(bet.get("odds"), errors="coerce"),
                "market name": market_lookup.get(bet.get("bet_id"), None),
                "legs": pd.to_numeric(bet.get("leg_count"), errors="coerce"),
            }
        )

    normalized = pd.DataFrame(normalized_rows)

    if normalized.empty:
        return normalized

    normalized["date"] = pd.to_datetime(normalized["date"], utc=True, errors="coerce").ffill()
    normalized["rank"] = normalized["rank"].fillna("unknown")
    normalized["ticket type"] = normalized["ticket type"].fillna("single")
    normalized["product"] = normalized["product"].fillna("unibet")

    for col, default in [("bets", 0.0), ("wins", 0.0), ("odds", 1.0), ("legs", 1)]:
        normalized[col] = pd.to_numeric(normalized[col], errors="coerce").fillna(default)

    if "market name" in normalized.columns:
        normalized["market name"] = normalized["market name"].fillna("").astype(str).str.strip()

    return normalized


__all__ = ["parse_unibet_paste", "normalize_unibet_paste"]
