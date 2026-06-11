from __future__ import annotations

from pathlib import Path
from typing import Optional

import duckdb

from db.schema import create_all_tables
from db.seed import seed_all


# DuckDB 파일 경로를 프로젝트 루트 기준으로 고정한다.
DB_FILE_NAME = "tarkov_loadout.duckdb"
_connection: Optional[duckdb.DuckDBPyConnection] = None


def get_db_path() -> Path:
    """프로젝트 루트에 생성되는 DB 파일 경로를 반환한다."""
    root_dir = Path(__file__).resolve().parent.parent
    return root_dir / DB_FILE_NAME


def get_connection() -> duckdb.DuckDBPyConnection:
    """싱글톤 방식으로 DB 연결을 재사용한다."""
    global _connection
    if _connection is None:
        _connection = duckdb.connect(str(get_db_path()))
    return _connection


def close_connection() -> None:
    """앱 종료 시 연결을 닫는다."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None


def initialize_database(seed: bool = True) -> None:
    """테이블 생성 후 선택적으로 시드 데이터를 입력한다."""
    conn = get_connection()
    create_all_tables(conn)
    if seed:
        seed_all(conn)
