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
                id, weapon_id, name, part_type, slot_name, recoil_delta, ergonomics_delta,
                accuracy_delta, weight, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["weapon_id"],
                data["name"],
                data["part_type"],
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
            SET weapon_id = ?, name = ?, part_type = ?, slot_name = ?, recoil_delta = ?,
                ergonomics_delta = ?, accuracy_delta = ?, weight = ?, description = ?
            WHERE id = ?
            """,
            (
                data["weapon_id"],
                data["name"],
                data["part_type"],
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

    def find_by_type(self, part_type: str) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon_part WHERE part_type = ? ORDER BY id",
            (part_type,),
        )

    def find_by_weapon_id(self, weapon_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon_part WHERE weapon_id = ? ORDER BY id",
            (weapon_id,),
        )

    def find_part_types(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT ROW_NUMBER() OVER (ORDER BY part_type) AS id, part_type AS name
            FROM (SELECT DISTINCT part_type FROM weapon_part)
            ORDER BY part_type
            """
        )
