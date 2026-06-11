from __future__ import annotations

from typing import Any

from repositories.armor_repository import ArmorRepository


class ArmorService:
    """방어구 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = ArmorRepository()

    def get_armors(self, armor_class: int | None = None) -> list[dict[str, Any]]:
        if armor_class is None:
            return self.repo.find_all()
        return self.repo.find_by_class(armor_class)

    def get_armor_detail(self, armor_id: int) -> dict[str, Any] | None:
        return self.repo.find_by_id(armor_id)

    def get_classes(self) -> list[int]:
        rows = self.repo.fetch_all("SELECT DISTINCT armor_class FROM armor ORDER BY armor_class")
        return [int(row["armor_class"]) for row in rows]
