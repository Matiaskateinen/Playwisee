"""Parser and normalizer for Unibet bet history pasted as raw text."""

from __future__ import annotations

import re
from datetime import datetime
from typing import List, Tuple

import pandas as pd


def _normalize_number(value: str) -> float | None:
    if not value:
        return None

    cleaned = value.replace("€", "").replace(" ", "")
    cleaned = re.sub(r"(\d),(?=\d{1,2}(\D|$))", r"\1.", cleaned)
    try:
        return float(cleaned)
    except ValueError:
        return None


def _extract_datetime(text: str) -> pd.Timestamp | None:
    # 12.12.2025 klo • 13.05.03
    match = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*klo\s*[•.]?\s*(\d{2}\.\d{2}\.\d{2})", text)
    if not match:
        return None

    date_part, time_part = match.groups()
    time_part = time_part.replace(".", ":")
    try:
        dt = datetime.strptime(f"{date_part} {time_part}", "%d.%m.%Y %H:%M:%S")
    except ValueError:
        return None

    return pd.Timestamp(dt, tz="UTC")

# Regex patterns shared by the splitter and tests
HEADER_PATTERN = re.compile(
    r"^(Single|TuplaVoitettu|Tupla|Tripla|Parlay|Tuplavoitettu)", re.IGNORECASE
)
COUPON_PATTERN = re.compile(r"^Kuponkitunnus:\s*\d+", re.IGNORECASE)

# Backwards compatibility: earlier versions referenced lowercase names
header_pattern = HEADER_PATTERN
coupon_pattern = COUPON_PATTERN


def _split_bets(raw_text: str) -> List[str]:
    """
    Split the pasted text into individual bet sections.

    Unibet pastes list a bet summary (e.g. ``Single`` header and odds) before
    the ``Kuponkitunnus`` line of that bet. We therefore stream through the
    lines and treat either a bet header *or* a coupon ID as the start of a new
    section, carrying any leading summary lines forward to the next coupon.
    """

    sections: List[str] = []
    current: List[str] = []
    pending: List[str] = []  # summary lines that should attach to the next coupon

    for raw_line in raw_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        if COUPON_PATTERN.match(line):
            if current:
                sections.append("\n".join(current).strip())
            current = pending + [line]
            pending = []
            continue

        if HEADER_PATTERN.match(line):
            if current:
                sections.append("\n".join(current).strip())
                current = []
            pending = [line]
            continue

        if current:
            current.append(line)
        else:
            pending.append(line)

    if current:
        sections.append("\n".join(current).strip())
    elif pending:
        sections.append("\n".join(pending).strip())

    return [s for s in sections if s]


def _parse_legs(lines: List[str], bet_id: str, overall_odds: float | None) -> List[dict]:
    legs: List[dict] = []
    skip_prefixes = {"kuponkitunnus", "kertoimet", "panos", "voitto"}

    for idx, line in enumerate(lines):
        if ":" not in line:
            continue
        key = line.split(":", 1)[0].strip().lower()
        if key in skip_prefixes:
            continue

        market, selection = [piece.strip() for piece in line.split(":", 1)]

        event = None
        for follow in lines[idx + 1 : idx + 4]:
            if " - " in follow:
                event = follow
                break

        window_text = " ".join(lines[idx : idx + 5])
        odds_match = re.search(r"([0-9]+[.,][0-9]+)", window_text)
        leg_odds = _normalize_number(odds_match.group(1)) if odds_match else None

        # Ignore metadata lines that aren't tied to a selection (e.g., score lines)
        if not event and leg_odds is None:
            continue

        legs.append(
            {
                "bet_id": bet_id,
                "event": event,
                "market": market or None,
                "selection": selection or None,
                "odds": leg_odds,
            }
        )

    if not legs:
        event_line = next((ln for ln in lines if " - " in ln), None)
        legs.append(
            {
                "bet_id": bet_id,
                "event": event_line,
                "market": None,
                "selection": None,
                "odds": overall_odds,
            }
        )

    return legs


def parse_unibet_paste(raw_text: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse Unibet bet history pasted as raw text.

    Returns:
        bets_df: One row per bet slip
        legs_df: One row per leg (for parlays)
    """

    cleaned = raw_text.replace("\r\n", "\n")
    cleaned = re.sub(r"(\d),(?=\d{1,2}\b)", r"\1.", cleaned)

    bet_sections = _split_bets(cleaned)
    bets: List[dict] = []
    legs: List[dict] = []

    for section in bet_sections:
        bet_id_match = re.search(r"Kuponkitunnus:\s*(\d+)", section)
        bet_id = bet_id_match.group(1) if bet_id_match else None

        placed_at = _extract_datetime(section)

        status_match = re.search(r"(Voitettu|Vireill[aä]|H[aä]vitty|Peruttu)", section, re.IGNORECASE)
        status = status_match.group(1).capitalize() if status_match else None

        bet_type_match = re.search(r"(Single|Tupla|Tripla|Parlay|Tupla|Tuplavoitettu)", section, re.IGNORECASE)
        bet_type = bet_type_match.group(1).capitalize() if bet_type_match else None
        if bet_type and bet_type.lower().startswith("tupla"):
            bet_type = "Tupla"

        stake_match = re.search(r"Panos:\s*€?([0-9.,]+)", section)
        stake = _normalize_number(stake_match.group(1)) if stake_match else None

        odds_match = re.search(r"Kertoimet:\s*([0-9.,]+)", section)
        if not odds_match:
            odds_match = re.search(r"@\s*([0-9.,]+)", section)
        odds = _normalize_number(odds_match.group(1)) if odds_match else None

        payout_match = re.search(r"Voitto:\s*€?([0-9.,]+)", section)
        payout = _normalize_number(payout_match.group(1)) if payout_match else None

        lines = [ln.strip() for ln in section.splitlines() if ln.strip()]
        section_legs = _parse_legs(lines, bet_id or "", odds)
        leg_count = len(section_legs)

        if not bet_type:
            if leg_count > 1:
                bet_type = "Parlay"
            else:
                bet_type = "Single"

        bets.append(
            {
                "bet_id": bet_id,
                "bookmaker": "Unibet",
                "placed_at": placed_at,
                "bet_type": bet_type,
                "stake": stake,
                "odds": odds,
                "payout": payout,
                "status": status,
                "leg_count": leg_count,
            }
        )
        legs.extend(section_legs)

    bets_df = pd.DataFrame(
        bets,
        columns=[
            "bet_id",
            "bookmaker",
            "placed_at",
            "bet_type",
            "stake",
            "odds",
            "payout",
            "status",
            "leg_count",
        ],
    )
    legs_df = pd.DataFrame(legs, columns=["bet_id", "event", "market", "selection", "odds"])

    # ensure datetime is UTC-aware
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

    # Attach a lightweight market label from the first leg when available
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
