from __future__ import annotations

from typing import Any

from repositories.helmet_repository import HelmetRepository


class HelmetService:
    """헬멧 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = HelmetRepository()

    def get_helmets(self, armor_class: int | None = None) -> list[dict[str, Any]]:
        if armor_class is None:
            return self.repo.find_all()
        return self.repo.find_by_class(armor_class)

    def get_helmet_detail(self, helmet_id: int) -> dict[str, Any] | None:
        return self.repo.find_by_id(helmet_id)

    def get_classes(self) -> list[int]:
        rows = self.repo.fetch_all("SELECT DISTINCT armor_class FROM helmet ORDER BY armor_class")
        return [int(row["armor_class"]) for row in rows]
