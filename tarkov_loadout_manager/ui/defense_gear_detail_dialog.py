from __future__ import annotations

import flet as ft


def open_defense_gear_detail_dialog(page: ft.Page, gear: dict) -> None:
    """방어 장비 상세 다이얼로그를 표시한다."""
    dialog = ft.AlertDialog(
        title=ft.Text(f"방어 장비 상세 - {gear['name']}"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(f"구분: {gear.get('gear_type', '-')}") ,
                    ft.Text(f"방어 등급: {gear.get('armor_class', '-')}") ,
                    ft.Text(f"내구도: {gear.get('durability', '-')}") ,
                    ft.Text(f"보호 부위: {gear.get('protected_area', '-')}") ,
                    ft.Text(f"재질: {gear.get('material', '-')}") ,
                    ft.Text(f"설명: {gear.get('description', '-')}") ,
                ],
            ),
        ),
        actions=[ft.TextButton("닫기", on_click=lambda _: _close(page, dialog))],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()


def _close(page: ft.Page, dialog: ft.AlertDialog) -> None:
    dialog.open = False
    page.update()
