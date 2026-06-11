from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class RigRepository(BaseRepository):
    """support_item(rig) CRUD."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM support_item WHERE item_type = 'rig' ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            "SELECT * FROM support_item WHERE id = ? AND item_type = 'rig'",
            (item_id,),
        )

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("support_item")
        self.execute(
            """
            INSERT INTO support_item (
                id, name, item_type, capacity_or_heal, uses_count, weight, effect_text, description
            ) VALUES (?, ?, 'rig', ?, NULL, ?, NULL, ?)
            """,
            (new_id, data["name"], data["slot_capacity"], data.get("weight"), data.get("description")),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE support_item
            SET name = ?, capacity_or_heal = ?, weight = ?, description = ?
            WHERE id = ? AND item_type = 'rig'
            """,
            (data["name"], data["slot_capacity"], data.get("weight"), data.get("description"), item_id),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM support_item WHERE id = ? AND item_type = 'rig'", (item_id,))
