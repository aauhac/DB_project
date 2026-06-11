from __future__ import annotations

import flet as ft


def open_part_detail_dialog(page: ft.Page, part: dict) -> None:
    """부품 상세 다이얼로그를 표시한다."""
    dialog = ft.AlertDialog(
        title=ft.Text(f"부품 상세 - {part['name']}"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(f"슬롯: {part.get('slot_name', '-')}") ,
                    ft.Text(f"반동 변화: {part.get('recoil_delta', 0)}") ,
                    ft.Text(f"에르고 변화: {part.get('ergonomics_delta', 0)}") ,
                    ft.Text(f"정확도 변화: {part.get('accuracy_delta', 0)}") ,
                    ft.Text(f"무게: {part.get('weight', '-')}") ,
                    ft.Text(f"설명: {part.get('description', '-')}") ,
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
