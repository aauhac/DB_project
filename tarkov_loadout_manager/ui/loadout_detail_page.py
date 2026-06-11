from __future__ import annotations

from typing import Callable

import flet as ft


def build_loadout_detail(
    detail: dict,
    on_edit: Callable[[], None],
    on_delete: Callable[[], None],
) -> ft.Control:
    """세팅 상세 화면 구성 컨트롤을 반환한다."""
    header = detail["header"]
    weapon = detail.get("weapon")

    def _named_item(name: str, value: str) -> ft.Control:
        return ft.Row([ft.Text(f"{name}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])

    weapon_name = weapon["name"] if weapon else "-"
    weapon_type = weapon.get("weapon_type_name", "-") if weapon else "-"

    parts = detail.get("weapon_parts", [])
    ammo_items = detail.get("ammo_items", [])
    medical_items = detail.get("medical_items", [])

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("세팅 상세", size=22, weight=ft.FontWeight.BOLD),
            _named_item("세팅명", str(header.get("name", "-"))),
            _named_item("작성자", str(header.get("nickname", "-"))),
            _named_item("생성일", str(header.get("created_at", "-"))),
            _named_item("메모", str(header.get("memo", ""))),
            ft.Divider(),
            _named_item("총기", weapon_name),
            _named_item("총기 유형", weapon_type),
            ft.Text("총기 부품", weight=ft.FontWeight.BOLD),
            ft.Column([ft.Text(f"- {item['name']} ({item.get('part_type_name', '-')})") for item in parts], spacing=4),
            ft.Divider(),
            ft.Text("탄약", weight=ft.FontWeight.BOLD),
            ft.Column([ft.Text(f"- {item['name']} x {item.get('quantity', 1)}") for item in ammo_items], spacing=4),
            ft.Divider(),
            _named_item("방어구", str((detail.get("armor") or {}).get("name", "-"))),
            _named_item("헬멧", str((detail.get("helmet") or {}).get("name", "-"))),
            _named_item("리그", str((detail.get("rig") or {}).get("name", "-"))),
            _named_item("백팩", str((detail.get("backpack") or {}).get("name", "-"))),
            ft.Divider(),
            ft.Text("의료품", weight=ft.FontWeight.BOLD),
            ft.Column([ft.Text(f"- {item['name']} x {item.get('quantity', 1)}") for item in medical_items], spacing=4),
            ft.Row([
                ft.ElevatedButton("수정", on_click=lambda _: on_edit()),
                ft.OutlinedButton("삭제", on_click=lambda _: on_delete()),
            ]),
        ],
    )
