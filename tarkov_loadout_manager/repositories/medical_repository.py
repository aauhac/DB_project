from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class MedicalRepository(BaseRepository):
    """medical_item 테이블 CRUD."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM medical_item ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM medical_item WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("medical_item")
        self.execute(
            """
            INSERT INTO medical_item (
                id, name, heal_amount, uses_count, effect_text, weight, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["name"],
                data.get("heal_amount"),
                data.get("uses_count"),
                data.get("effect_text"),
                data.get("weight"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE medical_item
            SET name = ?, heal_amount = ?, uses_count = ?, effect_text = ?, weight = ?, description = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data.get("heal_amount"),
                data.get("uses_count"),
                data.get("effect_text"),
                data.get("weight"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM medical_item WHERE id = ?", (item_id,))
