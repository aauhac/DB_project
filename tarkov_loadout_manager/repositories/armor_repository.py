from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class ArmorRepository(BaseRepository):
    """defense_gear(armor) 조회용 리포지토리."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM defense_gear WHERE gear_type = 'armor' ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            "SELECT * FROM defense_gear WHERE id = ? AND gear_type = 'armor'",
            (item_id,),
        )

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("defense_gear")
        self.execute(
            """
            INSERT INTO defense_gear (
                id, name, armor_class, durability, protected_area, material,
                move_speed_penalty, turn_speed_penalty, ergonomics_penalty, gear_type, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                "armor",
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE defense_gear
            SET name = ?, armor_class = ?, durability = ?, protected_area = ?,
                material = ?, move_speed_penalty = ?, turn_speed_penalty = ?,
                ergonomics_penalty = ?, description = ?
            WHERE id = ? AND gear_type = 'armor'
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
        self.execute("DELETE FROM defense_gear WHERE id = ? AND gear_type = 'armor'", (item_id,))

    def find_by_class(self, armor_class: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM defense_gear WHERE gear_type = 'armor' AND armor_class = ? ORDER BY id",
            (armor_class,),
        )
