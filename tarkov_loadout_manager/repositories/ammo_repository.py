from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class AmmoRepository(BaseRepository):
    """ammo 테이블 CRUD 및 조건 조회."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM ammo ORDER BY id")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM ammo WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        new_id = self.get_next_id("ammo")
        self.execute(
            """
            INSERT INTO ammo (
                id, name, caliber, damage, penetration, armor_damage_pct,
                recoil_modifier, velocity, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id,
                data["name"],
                data["caliber"],
                data["damage"],
                data["penetration"],
                data.get("armor_damage_pct"),
                data.get("recoil_modifier"),
                data.get("velocity"),
                data.get("description"),
            ),
        )
        return new_id

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.execute(
            """
            UPDATE ammo
            SET name = ?, caliber = ?, damage = ?, penetration = ?, armor_damage_pct = ?,
                recoil_modifier = ?, velocity = ?, description = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["caliber"],
                data["damage"],
                data["penetration"],
                data.get("armor_damage_pct"),
                data.get("recoil_modifier"),
                data.get("velocity"),
                data.get("description"),
                item_id,
            ),
        )

    def delete(self, item_id: int) -> None:
        self.execute("DELETE FROM ammo WHERE id = ?", (item_id,))

    def find_by_caliber(self, caliber: str) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM ammo WHERE caliber = ? ORDER BY id", (caliber,))
