"""Utilities for normalizing Coolbet exports for PlayWise.

The app expects a standard schema regardless of where data originates.
This module converts common Coolbet column names to the expected ones and
performs light type cleaning so other backends can follow the same
contract.
"""

from __future__ import annotations

from typing import Dict, Iterable

import pandas as pd


# Expected canonical columns used by the analytics UI
REQUIRED_COLUMNS = {"date", "rank", "ticket type", "product", "bets", "wins", "odds"}

# Common Coolbet export headers mapped to the canonical schema
COLUMN_ALIASES: Dict[str, Iterable[str]] = {
    "date": {"date", "placed", "bet date", "event date"},
    "rank": {"result", "status", "outcome"},
    "ticket type": {"ticket type", "bet type", "type"},
    "product": {"product", "channel", "platform"},
    "bets": {"stake", "bet amount", "wager", "bets"},
    "wins": {"wins", "return", "payout", "winnings"},
    "odds": {"odds", "total odds", "combined odds", "decimal odds"},
    "market name": {"market", "market name", "selection market"},
}


class NormalizationError(ValueError):
    """Raised when a Coolbet file cannot be normalized."""


def _apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    lower_to_original = {str(col).strip().lower(): col for col in df.columns}
    rename_map: Dict[str, str] = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_to_original:
                rename_map[lower_to_original[alias]] = canonical
                break

    return df.rename(columns=rename_map)


def _collapse_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Merge duplicate columns by forward-filling across them.

    Coolbet exports sometimes include both a canonical column (e.g. "rank") and
    a synonymous header (e.g. "result"). When normalized, both can map to the
    same canonical name, leaving duplicate column labels. Pandas then treats
    column selection as 2D, causing groupby to fail with "not 1-dimensional".
    This helper collapses duplicates to a single Series, preferring the first
    non-null value from left to right.
    """

    df = df.copy()
    seen = set()

    for col in df.columns:
        if col in seen:
            continue

        duplicates = [c for c in df.columns if c == col]
        if len(duplicates) > 1:
            merged = df[duplicates].bfill(axis=1).iloc[:, 0]
            df = df.drop(columns=duplicates).assign(**{col: merged})

        seen.add(col)

    return df


def normalize_coolbet_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe with canonical PlayWise columns.

    Args:
        df: Raw dataframe read from a Coolbet Excel export.

    Raises:
        NormalizationError: if required columns are missing after normalization.
    """

    normalized = df.copy()
    normalized.columns = [str(col).strip().lower() for col in normalized.columns]
    normalized = _apply_aliases(normalized)
    normalized = _collapse_duplicate_columns(normalized)

    missing = REQUIRED_COLUMNS - set(normalized.columns)
    if missing:
        raise NormalizationError(
            "Missing required columns after normalization: " + ", ".join(sorted(missing))
        )

    normalized["ticket type"] = normalized["ticket type"].astype(str)
    normalized["product"] = normalized["product"].astype(str)
    normalized["date"] = pd.to_datetime(normalized["date"].ffill())
    normalized["rank"] = normalized["rank"].ffill()

    for col in ["bets", "wins", "odds"]:
        normalized[col] = pd.to_numeric(normalized[col], errors="coerce")

    if "market name" in normalized.columns:
        normalized["market name"] = normalized["market name"].astype(str)

    return normalized


__all__ = ["NormalizationError", "normalize_coolbet_data"]
