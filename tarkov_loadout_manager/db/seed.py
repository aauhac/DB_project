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
        "INSERT OR IGNORE INTO user_account (id, email, nickname) VALUES (?, ?, ?)",
        [
            (1, "pmc@example.com", "PMC_KOR"),
            (2, "scav@example.com", "SCAV_LOVER"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO weapon_type (id, name) VALUES (?, ?)",
        [
            (1, "Assault Rifle"),
            (2, "SMG"),
            (3, "DMR"),
            (4, "Shotgun"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO weapon (
            id, weapon_type_id, name, caliber, manufacturer, recoil, ergonomics,
            fire_mode, weight, image_path, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, "AK-74M", "5.45x39", "Kalashnikov Concern", 68, 52, "Auto/Semi", 3.5, "", "균형 잡힌 기본 AR"),
            (2, 1, "M4A1", "5.56x45", "Colt", 61, 58, "Auto/Semi", 3.1, "", "커스터마이징 폭이 넓은 AR"),
            (3, 2, "MP5", "9x19", "HK", 45, 64, "Auto/Semi", 2.7, "", "반동이 낮은 근거리 SMG"),
            (4, 3, "SVDS", "7.62x54R", "Izhmash", 88, 40, "Semi", 4.3, "", "강력한 관통력을 가진 DMR"),
            (5, 4, "MP-153", "12/70", "Baikal", 95, 35, "Semi", 3.8, "", "근중거리에서 강력한 샷건"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO part_type (id, name) VALUES (?, ?)",
        [
            (1, "Scope"),
            (2, "Muzzle"),
            (3, "Stock"),
            (4, "Foregrip"),
            (5, "Magazine"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO weapon_part (
            id, part_type_id, name, slot_name, recoil_delta, ergonomics_delta,
            accuracy_delta, weight, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, "EKP-8-18", "Optic", -1, 2, 1, 0.3, "가성비 도트 사이트"),
            (2, 1, "SpecterDR", "Optic", -2, -1, 3, 0.6, "가변 배율 스코프"),
            (3, 2, "PBS-4", "Muzzle", -8, -2, 0, 0.5, "5.45 소음기"),
            (4, 2, "Wave QD", "Muzzle", -10, -3, 1, 0.6, "5.56 소음기"),
            (5, 3, "MOE Stock", "Stock", -5, 4, 0, 0.7, "M4 계열 개머리판"),
            (6, 3, "Zenit PT-3", "Stock", -7, 3, 0, 0.8, "AK 계열 개머리판"),
            (7, 4, "RK-1", "Foregrip", -6, -1, 0, 0.4, "반동 억제용 수직손잡이"),
            (8, 4, "AFG", "Foregrip", -3, 2, 0, 0.3, "에르고 개선형 손잡이"),
            (9, 5, "AK 60-round Mag", "Magazine", 1, -3, 0, 0.5, "AK 대용량 탄창"),
            (10, 5, "STANAG 60-round", "Magazine", 1, -4, 0, 0.5, "M4 대용량 탄창"),
            (11, 5, "MP5 50-round Drum", "Magazine", 2, -5, 0, 0.7, "MP5 드럼탄창"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO weapon_part_compatibility (id, weapon_id, weapon_part_id) VALUES (?, ?, ?)",
        [
            (1, 1, 1), (2, 1, 3), (3, 1, 6), (4, 1, 7), (5, 1, 9),
            (6, 2, 2), (7, 2, 4), (8, 2, 5), (9, 2, 8), (10, 2, 10),
            (11, 3, 1), (12, 3, 8), (13, 3, 11),
            (14, 4, 2), (15, 4, 7),
            (16, 5, 1),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO ammo (
            id, name, caliber, damage, penetration, armor_damage_pct,
            recoil_modifier, velocity, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "5.45 BP", "5.45x39", 48, 37, 55.0, 2, 890, "고관통 5.45 탄"),
            (2, "5.45 BT", "5.45x39", 44, 34, 52.0, 1, 880, "트레이서 포함 탄약"),
            (3, "5.56 M855A1", "5.56x45", 45, 44, 52.0, 2, 945, "대표적 5.56 고성능 탄"),
            (4, "9x19 AP 6.3", "9x19", 52, 30, 48.0, 1, 402, "SMG용 고관통 탄"),
            (5, "7.62x54R PS", "7.62x54R", 86, 45, 63.0, 3, 840, "DMR용 강력 탄"),
            (6, "12/70 AP-20", "12/70", 164, 37, 65.0, 8, 400, "슬러그 고관통 탄"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO armor (
            id, name, armor_class, durability, protected_area, material,
            move_speed_penalty, turn_speed_penalty, ergonomics_penalty, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "PACA", 2, 50, "Thorax", "Aramid", -2.0, -1.0, -1.0, "초반용 가벼운 방어구"),
            (2, "6B23-1", 3, 65, "Thorax/Stomach", "Titan", -6.0, -4.0, -5.0, "밸런스형 방탄복"),
            (3, "Trooper", 4, 85, "Thorax", "UHMWPE", -5.0, -3.0, -4.0, "중급자용 인기 방어구"),
            (4, "Gen4 Assault", 5, 95, "Thorax/Stomach/Arms", "Composite", -11.0, -8.0, -9.0, "고등급 중장갑"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO helmet (
            id, name, armor_class, durability, protected_area, material,
            sound_penalty, ricochet_chance, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "Kolpak", 2, 30, "Head", "Steel", -2.0, "Low", "가벼운 초반 헬멧"),
            (2, "Ratnik Helmet", 3, 45, "Head/Ears", "Aramid", -4.0, "Medium", "무난한 중급 헬멧"),
            (3, "ULACH", 4, 55, "Head/Ears", "UHMWPE", -5.0, "High", "고성능 헬멧"),
            (4, "Altyn", 5, 70, "Head/Face", "Titan", -8.0, "High", "중장갑 돌격용 헬멧"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO rig (id, name, slot_capacity, weight, description) VALUES (?, ?, ?, ?, ?)",
        [
            (1, "Scav Vest", 8, 1.1, "기본형 리그"),
            (2, "BlackRock", 16, 1.8, "밸런스 좋은 전술 리그"),
            (3, "AVS", 18, 2.2, "대용량 장비 운용 리그"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO backpack (id, name, capacity, weight, description) VALUES (?, ?, ?, ?, ?)",
        [
            (1, "MBSS", 16, 1.0, "초반용 소형 백팩"),
            (2, "Berkut", 20, 1.3, "중형 백팩"),
            (3, "Tri-Zip", 30, 2.0, "레이드용 대형 백팩"),
        ],
    )

    _insert_many(
        conn,
        """
        INSERT OR IGNORE INTO medical_item (
            id, name, heal_amount, uses_count, effect_text, weight, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "AI-2", 100, 1, "기본 회복", 0.2, "초반 응급 회복"),
            (2, "Salewa Kit", 400, 3, "출혈/체력 회복", 0.5, "범용 의료품"),
            (3, "IFAK", 300, 2, "출혈/체력 회복", 0.4, "컴팩트 의료품"),
            (4, "CMS Kit", 0, 5, "골절/부위 복구", 0.7, "수술 키트"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout (id, user_id, name, memo) VALUES (?, ?, ?, ?)",
        [
            (1, 1, "Dorms Rush", "근거리 교전 중심"),
            (2, 1, "Woods Midrange", "중거리 교전 중심"),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_weapon (id, loadout_id, weapon_id) VALUES (?, ?, ?)",
        [
            (1, 1, 3),
            (2, 2, 1),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_weapon_part (id, loadout_weapon_id, weapon_part_id) VALUES (?, ?, ?)",
        [
            (1, 1, 1),
            (2, 1, 8),
            (3, 1, 11),
            (4, 2, 1),
            (5, 2, 3),
            (6, 2, 6),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_ammo (id, loadout_id, ammo_id, quantity) VALUES (?, ?, ?, ?)",
        [
            (1, 1, 4, 4),
            (2, 2, 1, 6),
            (3, 2, 2, 2),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_armor (id, loadout_id, armor_id) VALUES (?, ?, ?)",
        [
            (1, 1, 2),
            (2, 2, 3),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_helmet (id, loadout_id, helmet_id) VALUES (?, ?, ?)",
        [
            (1, 1, 2),
            (2, 2, 3),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_rig (id, loadout_id, rig_id) VALUES (?, ?, ?)",
        [
            (1, 1, 2),
            (2, 2, 3),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_backpack (id, loadout_id, backpack_id) VALUES (?, ?, ?)",
        [
            (1, 1, 1),
            (2, 2, 2),
        ],
    )

    _insert_many(
        conn,
        "INSERT OR IGNORE INTO loadout_medical (id, loadout_id, medical_item_id, quantity) VALUES (?, ?, ?, ?)",
        [
            (1, 1, 2, 1),
            (2, 1, 4, 1),
            (3, 2, 3, 1),
            (4, 2, 4, 1),
        ],
    )
