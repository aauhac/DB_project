from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class WeaponPartRepository(BaseRepository):
    """weapon_part 테이블 CRUD 및 조건 조회."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM weapon_part ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM weapon_part WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("weapon_part")
        self.execute(
            """
            INSERT INTO weapon_part (
                id, part_type_id, name, slot_name, recoil_delta, ergonomics_delta,
                accuracy_delta, weight, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["part_type_id"],
                data["name"],
                data.get("slot_name"),
                data.get("recoil_delta"),
                data.get("ergonomics_delta"),
                data.get("accuracy_delta"),
                data.get("weight"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE weapon_part
            SET part_type_id = ?, name = ?, slot_name = ?, recoil_delta = ?,
                ergonomics_delta = ?, accuracy_delta = ?, weight = ?, description = ?
            WHERE id = ?
            """,
            (
                data["part_type_id"],
                data["name"],
                data.get("slot_name"),
                data.get("recoil_delta"),
                data.get("ergonomics_delta"),
                data.get("accuracy_delta"),
                data.get("weight"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM weapon_part WHERE id = ?", (item_id,))

    def find_by_type(self, part_type_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon_part WHERE part_type_id = ? ORDER BY id",
            (part_type_id,),
        )

    def find_by_weapon_id(self, weapon_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT *
            FROM weapon_part
            WHERE id IN (
                SELECT weapon_part_id
                FROM weapon_part_compatibility
                WHERE weapon_id = ?
            )
            ORDER BY id
            """,
            (weapon_id,),
        )

    def find_part_types(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM part_type ORDER BY id")
