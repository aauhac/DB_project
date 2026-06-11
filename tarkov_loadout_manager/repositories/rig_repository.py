from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class RigRepository(BaseRepository):
    """rig 테이블 CRUD."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM rig ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM rig WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("rig")
        self.execute(
            "INSERT INTO rig (id, name, slot_capacity, weight, description) VALUES (?, ?, ?, ?, ?)",
            (new_id, data["name"], data["slot_capacity"], data.get("weight"), data.get("description")),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            "UPDATE rig SET name = ?, slot_capacity = ?, weight = ?, description = ? WHERE id = ?",
            (data["name"], data["slot_capacity"], data.get("weight"), data.get("description"), item_id),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM rig WHERE id = ?", (item_id,))
