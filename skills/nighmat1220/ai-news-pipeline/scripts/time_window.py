from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


TIME_WINDOW_PATTERN = re.compile(
    r"^\s*"
    r"(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点(?:(\d{1,2})分?)?"
    r"\s*到\s*"
    r"(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})点(?:(\d{1,2})分?)?"
    r"\s*$"
)


def parse_time_window(value: str) -> tuple[datetime, datetime]:
    match = TIME_WINDOW_PATTERN.match(value)
    if not match:
        raise ValueError(
            "时间窗口格式无效，请使用“几几年几月几日几点到几几年几月几日几点”或带分钟的格式。"
        )

    groups = match.groups()
    start = datetime(
        year=int(groups[0]),
        month=int(groups[1]),
        day=int(groups[2]),
        hour=int(groups[3]),
        minute=int(groups[4] or 0),
    )
    end = datetime(
        year=int(groups[5]),
        month=int(groups[6]),
        day=int(groups[7]),
        hour=int(groups[8]),
        minute=int(groups[9] or 0),
    )
    if end < start:
        raise ValueError("时间窗口结束时间不能早于开始时间。")
    return start, end


def parse_record_datetime(value: str) -> datetime | None:
    cleaned = (value or "").strip()
    if not cleaned:
        return None

    try:
        dt = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return None

    if dt.tzinfo is not None:
        return dt.astimezone().replace(tzinfo=None)
    return dt


def in_time_window(value: str, start: datetime, end: datetime) -> bool:
    dt = parse_record_datetime(value)
    if dt is None:
        return False
    return start <= dt <= end


def target_date_strings_from_window(start: datetime, end: datetime, *, prefix: str = "") -> list[str]:
    dates: list[str] = []
    current = start.date()
    end_date = end.date()
    while current <= end_date:
        date_text = current.isoformat()
        dates.append(f"{prefix}{date_text}" if prefix else date_text)
        current = current.fromordinal(current.toordinal() + 1)
    return dates


def existing_paths_from_stems(base_dir: Path, stems: list[str], suffix: str = ".jsonl") -> list[Path]:
    paths: list[Path] = []
    for stem in stems:
        path = base_dir / f"{stem}{suffix}"
        if path.exists():
            paths.append(path)
    return paths
