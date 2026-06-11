from __future__ import annotations

from typing import Any, Iterable, Optional

import duckdb

from db.database import get_connection


class BaseRepository:
    """공통 DB 실행 유틸을 제공하는 베이스 리포지토리."""

    def __init__(self, conn: Optional[duckdb.DuckDBPyConnection] = None) -> None:
        self.conn = conn or get_connection()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
        cursor = self.conn.execute(sql, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[dict[str, Any]]:
        cursor = self.conn.execute(sql, params)
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    def execute(self, sql: str, params: Iterable[Any] = ()) -> None:
        self.conn.execute(sql, params)

    def executemany(self, sql: str, params_list: Iterable[Iterable[Any]]) -> None:
        for params in params_list:
            self.conn.execute(sql, params)

    def get_next_id(self, table: str) -> int:
        """ID 자동 증가가 없으므로 MAX(id)+1 방식으로 다음 ID를 계산한다."""
        row = self.fetch_one(f"SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM {table}")
        return int(row["next_id"]) if row else 1
