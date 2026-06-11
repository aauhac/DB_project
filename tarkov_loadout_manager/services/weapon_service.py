from __future__ import annotations

from typing import Any

from repositories.loadout_join_repository import LoadoutJoinRepository
from repositories.weapon_repository import WeaponRepository


class WeaponService:
    """총기 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.weapon_repo = WeaponRepository()
        self.join_repo = LoadoutJoinRepository()

    def get_weapons(self, name_keyword: str = "", weapon_type: str | None = None) -> list[dict[str, Any]]:
        if weapon_type is not None:
            items = self.weapon_repo.find_by_type(weapon_type)
        else:
            items = self.weapon_repo.find_all()

        if name_keyword.strip():
            key = name_keyword.lower()
            items = [item for item in items if key in str(item["name"]).lower()]
        return items

    def get_weapon_types(self) -> list[dict[str, Any]]:
        return self.weapon_repo.find_weapon_types()

    def get_weapon_detail(self, weapon_id: int) -> dict[str, Any] | None:
        return self.join_repo.find_weapon_detail_with_parts(weapon_id)
