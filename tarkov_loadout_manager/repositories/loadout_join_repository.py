from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class LoadoutJoinRepository(BaseRepository):
    """Join 조회 전용 리포지토리."""

    def find_weapon_detail_with_parts(self, weapon_id: int) -> dict[str, Any] | None:
        weapon = self.fetch_one(
            """
            SELECT *
            FROM weapon
            WHERE id = ?
            """,
            (weapon_id,),
        )
        if weapon is None:
            return None

        parts = self.fetch_all(
            """
            SELECT wp.*, wp.part_type AS part_type_name
            FROM weapon_part wp
            WHERE wp.weapon_id = ?
            ORDER BY wp.id
            """,
            (weapon_id,),
        )

        weapon["compatible_parts"] = parts
        return weapon

    def find_all_loadouts_summary(self, user_id: int) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT l.id, l.name, l.memo, l.created_at, u.nickname,
                   w.name AS weapon_name
            FROM loadout l
            JOIN app_user u ON l.user_id = u.id
            LEFT JOIN loadout_item li ON li.loadout_id = l.id AND li.item_category = 'weapon'
            LEFT JOIN weapon w ON li.item_id = w.id
            WHERE l.user_id = ?
            ORDER BY l.created_at DESC
            """,
            (user_id,),
        )

    def find_loadout_detail(self, loadout_id: int) -> dict[str, Any] | None:
        header = self.fetch_one(
            """
            SELECT l.id, l.name, l.raid_purpose, l.memo, l.created_at, u.id AS user_id, u.nickname, u.email
            FROM loadout l
            JOIN app_user u ON l.user_id = u.id
            WHERE l.id = ?
            """,
            (loadout_id,),
        )
        if header is None:
            return None

        weapon_items = self.fetch_all(
            """
            SELECT li.id AS loadout_item_id, li.quantity, li.slot_label, w.*,
                   w.weapon_category AS weapon_type_name
            FROM loadout_item li
            JOIN weapon w ON li.item_id = w.id
            WHERE li.loadout_id = ? AND li.item_category = 'weapon'
            """,
            (loadout_id,),
        )
        weapon = weapon_items[0] if weapon_items else None

        parts = self.fetch_all(
            """
            SELECT li.id AS loadout_item_id, li.quantity, li.slot_label, wp.*,
                   wp.part_type AS part_type_name
            FROM loadout_item li
            JOIN weapon_part wp ON li.item_id = wp.id
            WHERE li.loadout_id = ? AND li.item_category = 'weapon_part'
            ORDER BY wp.id
            """,
            (loadout_id,),
        )

        ammo_items = self.fetch_all(
            """
            SELECT li.id AS loadout_item_id, li.quantity, li.slot_label, a.*
            FROM loadout_item li
            JOIN ammo a ON li.item_id = a.id
            WHERE li.loadout_id = ? AND li.item_category = 'ammo'
            ORDER BY a.id
            """,
            (loadout_id,),
        )

        defense_gears = self.fetch_all(
            """
            SELECT li.id AS loadout_item_id, li.quantity, li.slot_label, dg.*
            FROM loadout_item li
            JOIN defense_gear dg ON li.item_id = dg.id
            WHERE li.loadout_id = ? AND li.item_category = 'defense_gear'
            ORDER BY dg.id
            """,
            (loadout_id,),
        )

        support_items = self.fetch_all(
            """
            SELECT li.id AS loadout_item_id, li.quantity, li.slot_label, si.*
            FROM loadout_item li
            JOIN support_item si ON li.item_id = si.id
            WHERE li.loadout_id = ? AND li.item_category = 'support_item'
            ORDER BY si.id
            """,
            (loadout_id,),
        )

        armor = next((item for item in defense_gears if item.get("gear_type") == "armor"), None)
        helmet = next((item for item in defense_gears if item.get("gear_type") == "helmet"), None)
        rig = next((item for item in support_items if item.get("item_type") == "rig"), None)
        backpack = next((item for item in support_items if item.get("item_type") == "backpack"), None)
        medical_items = [item for item in support_items if item.get("item_type") == "medical"]

        loadout_items = self.fetch_all(
            """
            SELECT id, item_category, item_id, quantity, slot_label
            FROM loadout_item
            WHERE loadout_id = ?
            ORDER BY id
            """,
            (loadout_id,),
        )

        return {
            "header": header,
            "weapon": weapon,
            "weapon_parts": parts,
            "ammo_items": ammo_items,
            "defense_gears": defense_gears,
            "support_items": support_items,
            "loadout_items": loadout_items,
            "armor": armor,
            "helmet": helmet,
            "rig": rig,
            "backpack": backpack,
            "medical_items": medical_items,
        }
