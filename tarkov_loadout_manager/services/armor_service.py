from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class ArmorService:
    """defense_gear 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = BaseRepository()

    def get_armors(self, armor_class: int | None = None, gear_type: str | None = None) -> list[dict[str, Any]]:
        sql = "SELECT * FROM defense_gear WHERE 1=1"
        params: list[Any] = []
        if armor_class is not None:
            sql += " AND armor_class = ?"
            params.append(armor_class)
        if gear_type:
            sql += " AND gear_type = ?"
            params.append(gear_type)
        sql += " ORDER BY id"
        return self.repo.fetch_all(sql, tuple(params))

    def get_armor_detail(self, armor_id: int) -> dict[str, Any] | None:
        return self.repo.fetch_one("SELECT * FROM defense_gear WHERE id = ?", (armor_id,))

    def get_classes(self, gear_type: str | None = None) -> list[int]:
        if gear_type:
            rows = self.repo.fetch_all(
                "SELECT DISTINCT armor_class FROM defense_gear WHERE gear_type = ? ORDER BY armor_class",
                (gear_type,),
            )
        else:
            rows = self.repo.fetch_all("SELECT DISTINCT armor_class FROM defense_gear ORDER BY armor_class")
        return [int(row["armor_class"]) for row in rows]
