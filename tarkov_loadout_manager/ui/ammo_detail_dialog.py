from __future__ import annotations

import flet as ft


def open_ammo_detail_dialog(page: ft.Page, ammo: dict) -> None:
    """탄약 상세 다이얼로그를 표시한다."""
    dialog = ft.AlertDialog(
        title=ft.Text(f"탄약 상세 - {ammo['name']}"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(f"구경: {ammo.get('caliber', '-')}") ,
                    ft.Text(f"데미지: {ammo.get('damage', '-')}") ,
                    ft.Text(f"관통력: {ammo.get('penetration', '-')}") ,
                    ft.Text(f"방어구 피해율: {ammo.get('armor_damage_pct', '-')}") ,
                    ft.Text(f"탄속: {ammo.get('velocity', '-')}") ,
                    ft.Text(f"설명: {ammo.get('description', '-')}") ,
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
