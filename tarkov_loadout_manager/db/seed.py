from __future__ import annotations

from typing import Sequence

import duckdb


def _insert_many(
    conn: duckdb.DuckDBPyConnection,
    sql: str,
    rows: Sequence[tuple],
) -> None:
    """중복 시 무시하면서 다건 데이터를 입력한다."""
    for row in rows:
        conn.execute(sql, row)


def seed_all(conn: duckdb.DuckDBPyConnection) -> None:
    """과제 데모용 기본 데이터를 삽입한다."""
    _insert_many(
        conn,
        "INSERT OR IGNORE INTO app_user (id, email, nickname) VALUES (?, ?, ?)",
        [
            (1, "pmc@example.com", "PMC_KOR"),
            (2, "scav@example.com", "SCAV_LOVER"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO weapon (
            id, name, weapon_category, caliber, manufacturer, recoil, ergonomics,
            fire_mode, weight, market_price, image_path, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "AK-74M", "Assault Rifle", "5.45x39", "Kalashnikov Concern", 68, 52, "Auto/Semi", 3.5, 75000, "", "균형 잡힌 기본 AR"),
            (2, "M4A1", "Assault Rifle", "5.56x45", "Colt", 61, 58, "Auto/Semi", 3.1, 120000, "", "커스터마이징 폭이 넓은 AR"),
            (3, "MP5", "SMG", "9x19", "HK", 45, 64, "Auto/Semi", 2.7, 58000, "", "반동이 낮은 근거리 SMG"),
            (4, "SVDS", "DMR", "7.62x54R", "Izhmash", 88, 40, "Semi", 4.3, 135000, "", "강력한 관통력을 가진 DMR"),
            (5, "MP-153", "Shotgun", "12/70", "Baikal", 95, 35, "Semi", 3.8, 42000, "", "근중거리에서 강력한 샷건"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO weapon_part (
            id, weapon_id, name, part_type, slot_name, recoil_delta, ergonomics_delta,
            accuracy_delta, weight, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, "EKP-8-18", "Scope", "Optic", -1, 2, 1, 0.3, "가성비 도트 사이트"),
            (2, 2, "SpecterDR", "Scope", "Optic", -2, -1, 3, 0.6, "가변 배율 스코프"),
            (3, 1, "PBS-4", "Muzzle", "Muzzle", -8, -2, 0, 0.5, "5.45 소음기"),
            (4, 2, "Wave QD", "Muzzle", "Muzzle", -10, -3, 1, 0.6, "5.56 소음기"),
            (5, 2, "MOE Stock", "Stock", "Stock", -5, 4, 0, 0.7, "M4 계열 개머리판"),
            (6, 1, "Zenit PT-3", "Stock", "Stock", -7, 3, 0, 0.8, "AK 계열 개머리판"),
            (7, 1, "RK-1", "Foregrip", "Foregrip", -6, -1, 0, 0.4, "반동 억제용 수직손잡이"),
            (8, 3, "AFG", "Foregrip", "Foregrip", -3, 2, 0, 0.3, "에르고 개선형 손잡이"),
            (9, 1, "AK 60-round Mag", "Magazine", "Magazine", 1, -3, 0, 0.5, "AK 대용량 탄창"),
            (10, 2, "STANAG 60-round", "Magazine", "Magazine", 1, -4, 0, 0.5, "M4 대용량 탄창"),
            (11, 3, "MP5 50-round Drum", "Magazine", "Magazine", 2, -5, 0, 0.7, "MP5 드럼탄창"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO ammo (
            id, name, caliber, damage, penetration, armor_damage_pct,
            recoil_modifier, velocity, market_price, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "5.45 BP", "5.45x39", 48, 37, 55.0, 2, 890, 900, "고관통 5.45 탄"),
            (2, "5.45 BT", "5.45x39", 44, 34, 52.0, 1, 880, 700, "트레이서 포함 탄약"),
            (3, "5.56 M855A1", "5.56x45", 45, 44, 52.0, 2, 945, 1400, "대표적 5.56 고성능 탄"),
            (4, "9x19 AP 6.3", "9x19", 52, 30, 48.0, 1, 402, 620, "SMG용 고관통 탄"),
            (5, "7.62x54R PS", "7.62x54R", 86, 45, 63.0, 3, 840, 1350, "DMR용 강력 탄"),
            (6, "12/70 AP-20", "12/70", 164, 37, 65.0, 8, 400, 800, "슬러그 고관통 탄"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO defense_gear (
            id, name, armor_class, durability, protected_area, material,
            move_speed_penalty, turn_speed_penalty, ergonomics_penalty,
            sound_penalty, ricochet_chance, gear_type, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "PACA", 2, 50, "Thorax", "Aramid", -2.0, -1.0, -1.0, None, None, "armor", "초반용 가벼운 방어구"),
            (2, "6B23-1", 3, 65, "Thorax/Stomach", "Titan", -6.0, -4.0, -5.0, None, None, "armor", "밸런스형 방탄복"),
            (3, "Ratnik Helmet", 3, 45, "Head/Ears", "Aramid", None, None, None, -4.0, "Medium", "helmet", "무난한 중급 헬멧"),
            (4, "ULACH", 4, 55, "Head/Ears", "UHMWPE", None, None, None, -5.0, "High", "helmet", "고성능 헬멧"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO support_item (
            id, name, item_type, capacity_or_heal, uses_count, weight, effect_text, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "Scav Vest", "rig", 8, None, 1.1, None, "기본형 리그"),
            (2, "Berkut", "backpack", 20, None, 1.3, None, "중형 백팩"),
            (3, "Salewa Kit", "medical", 400, 3, 0.5, "출혈/체력 회복", "범용 의료품"),
            (4, "CMS Kit", "medical", 0, 5, 0.7, "골절/부위 복구", "수술 키트"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout (id, user_id, name, raid_purpose, memo) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, "Dorms Rush", "CQB", "근거리 교전 중심"),
            (2, 1, "Woods Midrange", "Midrange", "중거리 교전 중심"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO loadout_item (
            id, loadout_id, item_category, item_id, quantity, slot_label
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, "weapon", 3, 1, "primary"),
            (2, 1, "weapon_part", 1, 1, "optic"),
            (3, 1, "weapon_part", 8, 1, "foregrip"),
            (4, 1, "ammo", 4, 4, "mag"),
            (5, 1, "defense_gear", 2, 1, "armor"),
            (6, 1, "defense_gear", 3, 1, "helmet"),
            (7, 1, "support_item", 1, 1, "rig"),
            (8, 1, "support_item", 3, 1, "medical"),
            (9, 2, "weapon", 1, 1, "primary"),
            (10, 2, "weapon_part", 3, 1, "muzzle"),
            (11, 2, "ammo", 1, 6, "reserve"),
            (12, 2, "defense_gear", 1, 1, "armor"),
            (13, 2, "support_item", 2, 1, "backpack"),
        ],
    )
