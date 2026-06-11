from __future__ import annotations

from typing import Any


def to_int_or_none(value: Any) -> int | None:
    """입력값을 정수로 변환하고 실패 시 None을 반환한다."""
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_str(value: Any) -> str:
    """None 안전 문자열 변환 함수."""
    return "" if value is None else str(value)
