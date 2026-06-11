from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class ArmorRepository(BaseRepository):
    """armor 테이블 CRUD 및 조건 조회."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM armor ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM armor WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("armor")
        self.execute(
            """
            INSERT INTO armor (
                id, name, armor_class, durability, protected_area, material,
                move_speed_penalty, turn_speed_penalty, ergonomics_penalty, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["name"],
                data["armor_class"],
                data["durability"],
                data.get("protected_area"),
                data.get("material"),
                data.get("move_speed_penalty"),
                data.get("turn_speed_penalty"),
                data.get("ergonomics_penalty"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE armor
            SET name = ?, armor_class = ?, durability = ?, protected_area = ?,
                material = ?, move_speed_penalty = ?, turn_speed_penalty = ?,
                ergonomics_penalty = ?, description = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["armor_class"],
                data["durability"],
                data.get("protected_area"),
                data.get("material"),
                data.get("move_speed_penalty"),
                data.get("turn_speed_penalty"),
                data.get("ergonomics_penalty"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM armor WHERE id = ?", (item_id,))

    def find_by_class(self, armor_class: int) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM armor WHERE armor_class = ? ORDER BY id", (armor_class,))
