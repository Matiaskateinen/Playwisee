"""Parser for Unibet bet history pasted as raw text."""

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


def _split_bets(raw_text: str) -> List[str]:
    # keep any header text with the first coupon
    parts = re.split(r"(?=Kuponkitunnus:\s*\d+)", raw_text)
    sections: List[str] = []
    buffer = ""
    for part in parts:
        if re.search(r"Kuponkitunnus:\s*\d+", part):
            sections.append(buffer + part)
            buffer = ""
        else:
            buffer += part
    if buffer and sections:
        sections[0] = buffer + sections[0]
    return [s.strip() for s in sections if s.strip()]


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

        odds_match = re.search(r"([0-9]+[.,][0-9]+)", " ".join(lines[idx : idx + 3]))
        leg_odds = _normalize_number(odds_match.group(1)) if odds_match else None

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

        bet_type_match = re.search(r"(Single|Tupla|Tripla|Parlay)", section, re.IGNORECASE)
        bet_type = bet_type_match.group(1).capitalize() if bet_type_match else None

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
            }
        )
        legs.extend(section_legs)

    bets_df = pd.DataFrame(bets, columns=["bet_id", "bookmaker", "placed_at", "bet_type", "stake", "odds", "payout", "status"])
    legs_df = pd.DataFrame(legs, columns=["bet_id", "event", "market", "selection", "odds"])

    # ensure datetime is UTC-aware
    if not bets_df.empty:
        bets_df["placed_at"] = pd.to_datetime(bets_df["placed_at"], utc=True, errors="coerce")
    return bets_df, legs_df


__all__ = ["parse_unibet_paste"]
