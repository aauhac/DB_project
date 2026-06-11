from __future__ import annotations

from typing import Any

from repositories.base_repository import BaseRepository


class LoadoutJoinRepository(BaseRepository):
    """Join 조회 전용 리포지토리."""

    def find_weapon_detail_with_parts(self, weapon_id: int) -> dict[str, Any] | None:
        weapon = self.fetch_one(
            """
            SELECT w.*, wt.name AS weapon_type_name
            FROM weapon w
            JOIN weapon_type wt ON w.weapon_type_id = wt.id
            WHERE w.id = ?
            """,
            (weapon_id,),
        )
        if weapon is None:
            return None

        parts = self.fetch_all(
            """
            SELECT wp.*, pt.name AS part_type_name
            FROM weapon_part_compatibility wpc
            JOIN weapon_part wp ON wpc.weapon_part_id = wp.id
            JOIN part_type pt ON wp.part_type_id = pt.id
            WHERE wpc.weapon_id = ?
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
            JOIN user_account u ON l.user_id = u.id
            LEFT JOIN loadout_weapon lw ON lw.loadout_id = l.id
            LEFT JOIN weapon w ON lw.weapon_id = w.id
            WHERE l.user_id = ?
            ORDER BY l.created_at DESC
            """,
            (user_id,),
        )

    def find_loadout_detail(self, loadout_id: int) -> dict[str, Any] | None:
        header = self.fetch_one(
            """
            SELECT l.id, l.name, l.memo, l.created_at, u.id AS user_id, u.nickname, u.email
            FROM loadout l
            JOIN user_account u ON l.user_id = u.id
            WHERE l.id = ?
            """,
            (loadout_id,),
        )
        if header is None:
            return None

        weapon = self.fetch_one(
            """
            SELECT lw.id AS loadout_weapon_id, w.*, wt.name AS weapon_type_name
            FROM loadout_weapon lw
            JOIN weapon w ON lw.weapon_id = w.id
            JOIN weapon_type wt ON w.weapon_type_id = wt.id
            WHERE lw.loadout_id = ?
            """,
            (loadout_id,),
        )

        parts: list[dict[str, Any]] = []
        if weapon is not None:
            parts = self.fetch_all(
                """
                SELECT wp.*, pt.name AS part_type_name
                FROM loadout_weapon_part lwp
                JOIN weapon_part wp ON lwp.weapon_part_id = wp.id
                JOIN part_type pt ON wp.part_type_id = pt.id
                WHERE lwp.loadout_weapon_id = ?
                ORDER BY wp.id
                """,
                (weapon["loadout_weapon_id"],),
            )

        ammo_items = self.fetch_all(
            """
            SELECT la.quantity, a.*
            FROM loadout_ammo la
            JOIN ammo a ON la.ammo_id = a.id
            WHERE la.loadout_id = ?
            ORDER BY a.id
            """,
            (loadout_id,),
        )

        armor = self.fetch_one(
            """
            SELECT a.*
            FROM loadout_armor la
            JOIN armor a ON la.armor_id = a.id
            WHERE la.loadout_id = ?
            """,
            (loadout_id,),
        )

        helmet = self.fetch_one(
            """
            SELECT h.*
            FROM loadout_helmet lh
            JOIN helmet h ON lh.helmet_id = h.id
            WHERE lh.loadout_id = ?
            """,
            (loadout_id,),
        )

        rig = self.fetch_one(
            """
            SELECT r.*
            FROM loadout_rig lr
            JOIN rig r ON lr.rig_id = r.id
            WHERE lr.loadout_id = ?
            """,
            (loadout_id,),
        )

        backpack = self.fetch_one(
            """
            SELECT b.*
            FROM loadout_backpack lb
            JOIN backpack b ON lb.backpack_id = b.id
            WHERE lb.loadout_id = ?
            """,
            (loadout_id,),
        )

        medical_items = self.fetch_all(
            """
            SELECT lm.quantity, mi.*
            FROM loadout_medical lm
            JOIN medical_item mi ON lm.medical_item_id = mi.id
            WHERE lm.loadout_id = ?
            ORDER BY mi.id
            """,
            (loadout_id,),
        )

        return {
            "header": header,
            "weapon": weapon,
            "weapon_parts": parts,
            "ammo_items": ammo_items,
            "armor": armor,
            "helmet": helmet,
            "rig": rig,
            "backpack": backpack,
            "medical_items": medical_items,
        }
