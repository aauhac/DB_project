from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class LoadoutRepository(BaseRepository):
    """loadout 및 하위 구성 테이블 저장/수정/삭제를 담당한다."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM loadout ORDER BY created_at DESC")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM loadout WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        return self.save_loadout_base(data["user_id"], data["name"], data.get("memo"))

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.update_loadout_base(item_id, data["name"], data.get("memo"))

    def delete(self, item_id: int) -> None:
        self.clear_loadout_children(item_id)
        self.execute("DELETE FROM loadout WHERE id = ?", (item_id,))

    def find_all_by_user(self, user_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM loadout WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )

    def save_loadout_base(self, user_id: int, name: str, memo: str | None) -> int:
        new_id = self.get_next_id("loadout")
        self.execute(
            "INSERT INTO loadout (id, user_id, name, memo) VALUES (?, ?, ?, ?)",
            (new_id, user_id, name, memo),
        )
        return new_id

    def update_loadout_base(self, loadout_id: int, name: str, memo: str | None) -> None:
        self.execute(
            "UPDATE loadout SET name = ?, memo = ? WHERE id = ?",
            (name, memo, loadout_id),
        )

    def clear_loadout_children(self, loadout_id: int) -> None:
        """수정/삭제 시 하위 데이터를 먼저 정리한다."""
        loadout_weapon = self.fetch_one(
            "SELECT id FROM loadout_weapon WHERE loadout_id = ?",
            (loadout_id,),
        )
        if loadout_weapon:
            self.execute(
                "DELETE FROM loadout_weapon_part WHERE loadout_weapon_id = ?",
                (loadout_weapon["id"],),
            )

        self.execute("DELETE FROM loadout_weapon WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_ammo WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_armor WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_helmet WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_rig WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_backpack WHERE loadout_id = ?", (loadout_id,))
        self.execute("DELETE FROM loadout_medical WHERE loadout_id = ?", (loadout_id,))

    def save_loadout_components(self, loadout_id: int, data: dict[str, Any]) -> None:
        """세팅 하위 구성 데이터를 삽입한다."""
        loadout_weapon_id = self.get_next_id("loadout_weapon")
        self.execute(
            "INSERT INTO loadout_weapon (id, loadout_id, weapon_id) VALUES (?, ?, ?)",
            (loadout_weapon_id, loadout_id, data["weapon_id"]),
        )

        part_rows = []
        next_part_id = self.get_next_id("loadout_weapon_part")
        for idx, part_id in enumerate(data.get("weapon_part_ids", [])):
            part_rows.append((next_part_id + idx, loadout_weapon_id, part_id))
        if part_rows:
            self.executemany(
                "INSERT INTO loadout_weapon_part (id, loadout_weapon_id, weapon_part_id) VALUES (?, ?, ?)",
                part_rows,
            )

        ammo_rows = []
        next_ammo_id = self.get_next_id("loadout_ammo")
        for idx, ammo_item in enumerate(data.get("ammo_items", [])):
            ammo_rows.append(
                (next_ammo_id + idx, loadout_id, ammo_item["ammo_id"], ammo_item["quantity"])
            )
        if ammo_rows:
            self.executemany(
                "INSERT INTO loadout_ammo (id, loadout_id, ammo_id, quantity) VALUES (?, ?, ?, ?)",
                ammo_rows,
            )

        if data.get("armor_id") is not None:
            self.execute(
                "INSERT INTO loadout_armor (id, loadout_id, armor_id) VALUES (?, ?, ?)",
                (self.get_next_id("loadout_armor"), loadout_id, data["armor_id"]),
            )

        if data.get("helmet_id") is not None:
            self.execute(
                "INSERT INTO loadout_helmet (id, loadout_id, helmet_id) VALUES (?, ?, ?)",
                (self.get_next_id("loadout_helmet"), loadout_id, data["helmet_id"]),
            )

        if data.get("rig_id") is not None:
            self.execute(
                "INSERT INTO loadout_rig (id, loadout_id, rig_id) VALUES (?, ?, ?)",
                (self.get_next_id("loadout_rig"), loadout_id, data["rig_id"]),
            )

        if data.get("backpack_id") is not None:
            self.execute(
                "INSERT INTO loadout_backpack (id, loadout_id, backpack_id) VALUES (?, ?, ?)",
                (self.get_next_id("loadout_backpack"), loadout_id, data["backpack_id"]),
            )

        medical_rows = []
        next_medical_id = self.get_next_id("loadout_medical")
        for idx, med_item in enumerate(data.get("medical_items", [])):
            medical_rows.append(
                (next_medical_id + idx, loadout_id, med_item["medical_item_id"], med_item["quantity"])
            )
        if medical_rows:
            self.executemany(
                "INSERT INTO loadout_medical (id, loadout_id, medical_item_id, quantity) VALUES (?, ?, ?, ?)",
                medical_rows,
            )
