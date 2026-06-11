from __future__ import annotations

from typing import Any


def is_blank(value: str | None) -> bool:
    """문자열이 비어 있는지 검사한다."""
    return value is None or value.strip() == ""


def validate_positive_int(value: Any) -> bool:
    """1 이상의 정수인지 검사한다."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value >= 1
    if isinstance(value, str) and value.isdigit():
        return int(value) >= 1
    return False


def validate_none_allowed(value: Any, allow_none: bool = True) -> bool:
    """None 허용 여부를 검사한다."""
    if value is None and not allow_none:
        return False
    return True


def validate_loadout_payload(payload: dict[str, Any]) -> tuple[bool, str]:
    """세팅 저장 전 필수 입력값을 검사한다."""
    if is_blank(payload.get("name")):
        return False, "세팅 이름은 비어 있을 수 없습니다."

    if payload.get("weapon_id") is None:
        return False, "총기를 반드시 선택해야 합니다."

    for ammo in payload.get("ammo_items", []):
        if not validate_positive_int(ammo.get("quantity")):
            return False, "탄약 수량은 1 이상의 정수여야 합니다."

    for medical in payload.get("medical_items", []):
        if not validate_positive_int(medical.get("quantity")):
            return False, "의료품 수량은 1 이상의 정수여야 합니다."

    return True, "검증 성공"
