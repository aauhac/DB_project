from __future__ import annotations

import flet as ft


def open_weapon_detail_dialog(
    page: ft.Page,
    weapon_detail: dict,
) -> None:
    """총기 상세 다이얼로그를 표시한다."""
    parts = weapon_detail.get("compatible_parts", [])
    image_path = weapon_detail.get("image_path")

    image_control: ft.Control
    if image_path:
        image_control = ft.Image(src=image_path, width=220, height=140, fit=ft.ImageFit.CONTAIN)
    else:
        image_control = ft.Container(
            content=ft.Text("이미지 없음", color="white"),
            bgcolor="#666666",
            width=220,
            height=140,
            alignment=ft.alignment.center,
            border_radius=8,
        )

    parts_list = ft.Column(
        controls=[ft.Text(f"- {part['name']} ({part['part_type_name']})") for part in parts],
        tight=True,
        spacing=4,
        scroll=ft.ScrollMode.AUTO,
        height=180,
    )

    dialog = ft.AlertDialog(
        title=ft.Text(f"총기 상세 - {weapon_detail['name']}"),
        content=ft.Container(
            width=540,
            content=ft.Column(
                controls=[
                    image_control,
                    ft.Text(f"유형: {weapon_detail.get('weapon_type_name', '-')}") ,
                    ft.Text(f"구경: {weapon_detail.get('caliber', '-')}") ,
                    ft.Text(f"제조사: {weapon_detail.get('manufacturer', '-')}") ,
                    ft.Text(f"반동: {weapon_detail.get('recoil', '-')}, 에르고: {weapon_detail.get('ergonomics', '-')}") ,
                    ft.Text(f"설명: {weapon_detail.get('description', '-')}") ,
                    ft.Divider(),
                    ft.Text("호환 부품"),
                    parts_list,
                ],
                tight=True,
                spacing=8,
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
