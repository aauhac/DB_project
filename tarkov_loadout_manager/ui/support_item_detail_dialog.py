from __future__ import annotations

import flet as ft


def open_support_item_detail_dialog(page: ft.Page, category_label: str, item: dict) -> None:
    """보조 장비 상세 다이얼로그를 표시한다."""
    controls = [ft.Text(f"이름: {item.get('name', '-')}")]
    for key, value in item.items():
        if key == "name":
            continue
        controls.append(ft.Text(f"{key}: {value}"))

    dialog = ft.AlertDialog(
        title=ft.Text(f"{category_label} 상세"),
        content=ft.Container(
            width=430,
            content=ft.Column(tight=True, scroll=ft.ScrollMode.AUTO, controls=controls),
        ),
        actions=[ft.TextButton("닫기", on_click=lambda _: _close(page, dialog))],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()


def _close(page: ft.Page, dialog: ft.AlertDialog) -> None:
    dialog.open = False
    page.update()
