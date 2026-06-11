from __future__ import annotations

from typing import List

import duckdb


# 각 테이블 생성 SQL을 FK 의존성 순서로 배치한다.
SCHEMA_SQLS: List[str] = [
    """
    -- 앱 사용자 정보 테이블
    CREATE TABLE IF NOT EXISTS app_user (
        id BIGINT PRIMARY KEY,
        email VARCHAR(100) UNIQUE NOT NULL,
        nickname VARCHAR(50) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    -- 총기 기본 정보 테이블
    CREATE TABLE IF NOT EXISTS weapon (
        id BIGINT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        weapon_category VARCHAR(50) NOT NULL,
        caliber VARCHAR(30) NOT NULL,
        manufacturer VARCHAR(100),
        recoil INT,
        ergonomics INT,
        fire_mode VARCHAR(50),
        weight DOUBLE,
        market_price INT,
        image_path VARCHAR(255),
        description TEXT
    );
    """,
    """
    -- 총기 전용 부품 테이블 (어느 총기용인지 weapon_id로 연결)
    CREATE TABLE IF NOT EXISTS weapon_part (
        id BIGINT PRIMARY KEY,
        weapon_id BIGINT NOT NULL,
        name VARCHAR(100) NOT NULL,
        part_type VARCHAR(50) NOT NULL,
        slot_name VARCHAR(50),
        recoil_delta INT,
        ergonomics_delta INT,
        accuracy_delta INT,
        weight DOUBLE,
        description TEXT,
        FOREIGN KEY (weapon_id) REFERENCES weapon(id)
    );
    """,
    """
    -- 탄약 테이블
    CREATE TABLE IF NOT EXISTS ammo (
        id BIGINT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        caliber VARCHAR(30) NOT NULL,
        damage INT NOT NULL,
        penetration INT NOT NULL,
        armor_damage_pct DOUBLE,
        recoil_modifier INT,
        velocity INT,
        market_price INT,
        description TEXT
    );
    """,
    """
    -- 방어 장비 통합 테이블 (armor/helmet 통합)
    CREATE TABLE IF NOT EXISTS defense_gear (
        id BIGINT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        gear_type VARCHAR(30) NOT NULL,
        armor_class INT NOT NULL,
        durability INT NOT NULL,
        protected_area VARCHAR(100),
        material VARCHAR(50),
        move_speed_penalty DOUBLE,
        turn_speed_penalty DOUBLE,
        ergonomics_penalty DOUBLE,
        sound_penalty DOUBLE,
        ricochet_chance VARCHAR(30),
        description TEXT
    );
    """,
    """
    -- 보조 장비 통합 테이블 (rig/backpack/medical 통합)
    CREATE TABLE IF NOT EXISTS support_item (
        id BIGINT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        item_type VARCHAR(30) NOT NULL,
        capacity_or_heal INT,
        uses_count INT,
        weight DOUBLE,
        effect_text TEXT,
        description TEXT
    );
    """,
    """
    -- 세팅 기본 정보 테이블
    CREATE TABLE IF NOT EXISTS loadout (
        id BIGINT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        name VARCHAR(100) NOT NULL,
        raid_purpose VARCHAR(50),
        memo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, name),
        FOREIGN KEY (user_id) REFERENCES app_user(id)
    );
    """,
    """
    -- 세팅 구성 아이템 테이블
    CREATE TABLE IF NOT EXISTS loadout_item (
        id BIGINT PRIMARY KEY,
        loadout_id BIGINT NOT NULL,
        item_category VARCHAR(30) NOT NULL,
        item_id BIGINT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        slot_label VARCHAR(50),
        FOREIGN KEY (loadout_id) REFERENCES loadout(id)
    );
    """,
]


def create_all_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """정의된 전체 DDL을 순서대로 실행한다."""
    for sql in SCHEMA_SQLS:
        conn.execute(sql)
