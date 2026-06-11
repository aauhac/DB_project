from __future__ import annotations

from typing import Any

from repositories.weapon_part_repository import WeaponPartRepository


class WeaponPartService:
    """총기 부품 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = WeaponPartRepository()

    def get_parts(self, part_type: str | None = None) -> list[dict[str, Any]]:
        if part_type is None:
            return self.repo.find_all()
        return self.repo.find_by_type(part_type)

    def get_part_types(self) -> list[dict[str, Any]]:
        return self.repo.find_part_types()

    def get_part_detail(self, part_id: int) -> dict[str, Any] | None:
        return self.repo.find_by_id(part_id)

    def get_parts_by_weapon(self, weapon_id: int) -> list[dict[str, Any]]:
        return self.repo.find_by_weapon_id(weapon_id)
