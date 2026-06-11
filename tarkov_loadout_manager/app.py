from __future__ import annotations

import flet as ft

from db.database import initialize_database
from ui.main_layout import MainLayout


def main(page: ft.Page) -> None:
    """Flet 앱 메인 엔트리 포인트."""
    page.title = "Escape from Tarkov 장비 세팅 관리 시스템"
    page.window_width = 1400
    page.window_height = 900

    # 앱 시작 시 DB 스키마/시드 데이터를 초기화한다.
    initialize_database(seed=True)

    layout = MainLayout(page)
    page.add(layout.build())


if __name__ == "__main__":
    ft.run(main)
