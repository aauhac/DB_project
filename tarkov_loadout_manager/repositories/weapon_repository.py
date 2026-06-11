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
                id, name, weapon_category, caliber, manufacturer, recoil, ergonomics,
                fire_mode, weight, market_price, image_path, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["name"],
                data["weapon_category"],
                data["caliber"],
                data.get("manufacturer"),
                data.get("recoil"),
                data.get("ergonomics"),
                data.get("fire_mode"),
                data.get("weight"),
                data.get("market_price"),
                data.get("image_path"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE weapon
            SET name = ?, weapon_category = ?, caliber = ?, manufacturer = ?, recoil = ?,
                ergonomics = ?, fire_mode = ?, weight = ?, market_price = ?, image_path = ?, description = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["weapon_category"],
                data["caliber"],
                data.get("manufacturer"),
                data.get("recoil"),
                data.get("ergonomics"),
                data.get("fire_mode"),
                data.get("weight"),
                data.get("market_price"),
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

    def find_by_type(self, weapon_category: str) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM weapon WHERE weapon_category = ? ORDER BY id",
            (weapon_category,),
        )

    def find_weapon_types(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT ROW_NUMBER() OVER (ORDER BY weapon_category) AS id, weapon_category AS name
            FROM (SELECT DISTINCT weapon_category FROM weapon)
            ORDER BY weapon_category
            """
        )
