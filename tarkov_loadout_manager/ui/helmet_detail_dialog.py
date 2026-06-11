from __future__ import annotations

import flet as ft


def open_helmet_detail_dialog(page: ft.Page, helmet: dict) -> None:
    """헬멧 상세 다이얼로그를 표시한다."""
    dialog = ft.AlertDialog(
        title=ft.Text(f"헬멧 상세 - {helmet['name']}"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(f"방어 등급: {helmet.get('armor_class', '-')}") ,
                    ft.Text(f"내구도: {helmet.get('durability', '-')}") ,
                    ft.Text(f"보호 부위: {helmet.get('protected_area', '-')}") ,
                    ft.Text(f"도탄 확률: {helmet.get('ricochet_chance', '-')}") ,
                    ft.Text(f"설명: {helmet.get('description', '-')}") ,
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
