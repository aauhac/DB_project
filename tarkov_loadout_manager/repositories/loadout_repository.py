from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class LoadoutRepository(BaseRepository):
    """loadout + loadout_item 저장/수정/삭제를 담당한다."""

    def find_all(self) -> list[dict[str, Any]]:
        return self.fetch_all("SELECT * FROM loadout ORDER BY created_at DESC")

    def find_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.fetch_one("SELECT * FROM loadout WHERE id = ?", (item_id,))

    def insert(self, data: dict[str, Any]) -> int:
        return self.save_loadout_base(
            data["user_id"],
            data["name"],
            data.get("raid_purpose"),
            data.get("memo"),
        )

    def update(self, item_id: int, data: dict[str, Any]) -> None:
        self.update_loadout_base(item_id, data["name"], data.get("raid_purpose"), data.get("memo"))

    def delete(self, item_id: int) -> None:
        self.clear_loadout_children(item_id)
        self.execute("DELETE FROM loadout WHERE id = ?", (item_id,))

    def find_all_by_user(self, user_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            "SELECT * FROM loadout WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )

    def save_loadout_base(
        self,
        user_id: int,
        name: str,
        raid_purpose: str | None,
        memo: str | None,
    ) -> int:
        new_id = self.get_next_id("loadout")
        self.execute(
            "INSERT INTO loadout (id, user_id, name, raid_purpose, memo) VALUES (?, ?, ?, ?, ?)",
            (new_id, user_id, name, raid_purpose, memo),
        )
        return new_id

    def update_loadout_base(
        self,
        loadout_id: int,
        name: str,
        raid_purpose: str | None,
        memo: str | None,
    ) -> None:
        self.execute(
            "UPDATE loadout SET name = ?, raid_purpose = ?, memo = ? WHERE id = ?",
            (name, raid_purpose, memo, loadout_id),
        )

    def clear_loadout_children(self, loadout_id: int) -> None:
        self.execute("DELETE FROM loadout_item WHERE loadout_id = ?", (loadout_id,))

    def save_loadout_components(self, loadout_id: int, data: dict[str, Any]) -> None:
        """세팅 하위 구성 데이터를 loadout_item으로 통합 저장한다."""
        rows: list[tuple[int, int, str, int, int, str | None]] = []
        next_id = self.get_next_id("loadout_item")

        def _push(category: str, item_id: int | None, quantity: int = 1, slot_label: str | None = None) -> None:
            nonlocal next_id
            if item_id is None:
                return
            rows.append((next_id, loadout_id, category, int(item_id), int(quantity), slot_label))
            next_id += 1

        _push("weapon", data.get("weapon_id"), 1, "primary")

        for part_id in data.get("weapon_part_ids", []):
            _push("weapon_part", int(part_id), 1, "part")

        for ammo_item in data.get("ammo_items", []):
            _push("ammo", ammo_item.get("ammo_id"), int(ammo_item.get("quantity", 1)), "ammo")

        _push("defense_gear", data.get("armor_id"), 1, "armor")
        _push("defense_gear", data.get("helmet_id"), 1, "helmet")

        _push("support_item", data.get("rig_id"), 1, "rig")
        _push("support_item", data.get("backpack_id"), 1, "backpack")

        for med_item in data.get("medical_items", []):
            _push("support_item", med_item.get("medical_item_id"), int(med_item.get("quantity", 1)), "medical")

        for support_item in data.get("support_items", []):
            _push(
                "support_item",
                support_item.get("support_item_id"),
                int(support_item.get("quantity", 1)),
                support_item.get("slot_label"),
            )

        if rows:
            self.executemany(
                """
                INSERT INTO loadout_item (
                    id, loadout_id, item_category, item_id, quantity, slot_label
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
