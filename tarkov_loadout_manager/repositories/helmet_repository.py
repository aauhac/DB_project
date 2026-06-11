from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class HelmetRepository(BaseRepository):
    """helmet 테이블 CRUD 및 조건 조회."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM helmet ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM helmet WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("helmet")
        self.execute(
            """
            INSERT INTO helmet (
                id, name, armor_class, durability, protected_area, material,
                sound_penalty, ricochet_chance, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["name"],
                data["armor_class"],
                data["durability"],
                data.get("protected_area"),
                data.get("material"),
                data.get("sound_penalty"),
                data.get("ricochet_chance"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE helmet
            SET name = ?, armor_class = ?, durability = ?, protected_area = ?, material = ?,
                sound_penalty = ?, ricochet_chance = ?, description = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["armor_class"],
                data["durability"],
                data.get("protected_area"),
                data.get("material"),
                data.get("sound_penalty"),
                data.get("ricochet_chance"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM helmet WHERE id = ?", (item_id,))

    def find_by_class(self, armor_class: int) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM helmet WHERE armor_class = ? ORDER BY id", (armor_class,))
