from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class BackpackRepository(BaseRepository):
    """backpack 테이블 CRUD."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM backpack ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM backpack WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("backpack")
        self.execute(
            "INSERT INTO backpack (id, name, capacity, weight, description) VALUES (?, ?, ?, ?, ?)",
            (new_id, data["name"], data["capacity"], data.get("weight"), data.get("description")),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            "UPDATE backpack SET name = ?, capacity = ?, weight = ?, description = ? WHERE id = ?",
            (data["name"], data["capacity"], data.get("weight"), data.get("description"), item_id),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM backpack WHERE id = ?", (item_id,))
