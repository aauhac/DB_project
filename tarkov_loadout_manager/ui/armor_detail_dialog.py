from __future__ import annotations

import flet as ft


def open_armor_detail_dialog(page: ft.Page, armor: dict) -> None:
    """방어구 상세 다이얼로그를 표시한다."""
    dialog = ft.AlertDialog(
        title=ft.Text(f"방어구 상세 - {armor['name']}"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(f"방어 등급: {armor.get('armor_class', '-')}") ,
                    ft.Text(f"내구도: {armor.get('durability', '-')}") ,
                    ft.Text(f"보호 부위: {armor.get('protected_area', '-')}") ,
                    ft.Text(f"재질: {armor.get('material', '-')}") ,
                    ft.Text(f"설명: {armor.get('description', '-')}") ,
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
