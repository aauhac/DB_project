from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class HelmetService:
    """defense_gear의 helmet 조회 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = BaseRepository()

    def get_helmets(self, armor_class: int | None = None) -> list[dict[str, Any]]:
        if armor_class is None:
            return self.repo.fetch_all(
                "SELECT * FROM defense_gear WHERE gear_type = 'helmet' ORDER BY id"
            )
        return self.repo.fetch_all(
            "SELECT * FROM defense_gear WHERE gear_type = 'helmet' AND armor_class = ? ORDER BY id",
            (armor_class,),
        )

    def get_helmet_detail(self, helmet_id: int) -> dict[str, Any] | None:
        return self.repo.fetch_one(
            "SELECT * FROM defense_gear WHERE gear_type = 'helmet' AND id = ?",
            (helmet_id,),
        )

    def get_classes(self) -> list[int]:
        rows = self.repo.fetch_all(
            "SELECT DISTINCT armor_class FROM defense_gear WHERE gear_type = 'helmet' ORDER BY armor_class"
        )
        return [int(row["armor_class"]) for row in rows]
