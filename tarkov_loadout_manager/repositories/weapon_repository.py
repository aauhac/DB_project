from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class WeaponRepository(BaseRepository):
    """weapon 테이블 CRUD 및 조건 조회."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM weapon ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM weapon WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("weapon")
        self.execute(
            """
            INSERT INTO weapon (
                id, weapon_type_id, name, caliber, manufacturer, recoil, ergonomics,
                fire_mode, weight, image_path, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["weapon_type_id"],
                data["name"],
                data["caliber"],
                data.get("manufacturer"),
                data.get("recoil"),
                data.get("ergonomics"),
                data.get("fire_mode"),
                data.get("weight"),
                data.get("image_path"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE weapon
            SET weapon_type_id = ?, name = ?, caliber = ?, manufacturer = ?, recoil = ?,
                ergonomics = ?, fire_mode = ?, weight = ?, image_path = ?, description = ?
            WHERE id = ?
            """,
            (
                data["weapon_type_id"],
                data["name"],
                data["caliber"],
                data.get("manufacturer"),
                data.get("recoil"),
                data.get("ergonomics"),
                data.get("fire_mode"),
                data.get("weight"),
                data.get("image_path"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM weapon WHERE id = ?", (item_id,))

    def find_by_name(self, keyword: str) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon WHERE name ILIKE ? ORDER BY id",
            (f"%{keyword}%",),
        )

    def find_by_type(self, weapon_type_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon WHERE weapon_type_id = ? ORDER BY id",
            (weapon_type_id,),
        )

    def find_weapon_types(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM weapon_type ORDER BY id")
