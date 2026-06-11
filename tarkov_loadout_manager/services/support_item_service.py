from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class SupportItemService:
    """support_item 통합 조회 서비스."""

    def __init__(self) -> None:
        self.repo = BaseRepository()

    def get_rigs(self) -> list[dict[str, Any]]:
        return self.repo.fetch_all(
            "SELECT * FROM support_item WHERE item_type = 'rig' ORDER BY id"
        )

    def get_backpacks(self) -> list[dict[str, Any]]:
        return self.repo.fetch_all(
            "SELECT * FROM support_item WHERE item_type = 'backpack' ORDER BY id"
        )

    def get_medicals(self) -> list[dict[str, Any]]:
        return self.repo.fetch_all(
            "SELECT * FROM support_item WHERE item_type = 'medical' ORDER BY id"
        )

    def get_support_item_detail(self, category: str, item_id: int) -> dict[str, Any] | None:
        item_type = "medical" if category == "medical_item" else category
        return self.repo.fetch_one(
            "SELECT * FROM support_item WHERE id = ? AND item_type = ?",
            (item_id, item_type),
        )
