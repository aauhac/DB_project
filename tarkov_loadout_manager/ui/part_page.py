from __future__ import annotations

import flet as ft

from services.weapon_part_service import WeaponPartService
from ui.part_detail_dialog import open_part_detail_dialog


class PartPage:
    """부품 목록/필터 UI."""

    def __init__(self, page: ft.Page, service: WeaponPartService) -> None:
        self.page = page
        self.service = service
        self.type_dropdown = ft.Dropdown(label="부품 유형", width=200)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("이름")),
                ft.DataColumn(ft.Text("슬롯")),
                ft.DataColumn(ft.Text("반동 변화")),
                ft.DataColumn(ft.Text("에르고 변화")),
            ],
            rows=[],
        )
        self.type_dropdown.on_change = lambda _: self.refresh()
        self._load_type_options()
        self.refresh()

    def _load_type_options(self) -> None:
        types = self.service.get_part_types()
        self.type_dropdown.options = [ft.dropdown.Option("", "전체")]
        self.type_dropdown.options.extend(
            [ft.dropdown.Option(str(item["name"]), str(item["name"])) for item in types]
        )

    def refresh(self) -> None:
        type_value = self.type_dropdown.value
        type_name = type_value if type_value else None
        parts = self.service.get_parts(type_name)

        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item["id"]))),
                    ft.DataCell(
                        ft.TextButton(
                            item["name"],
                            on_click=lambda _, pid=item["id"]: self._open_detail(pid),
                        )
                    ),
                    ft.DataCell(ft.Text(str(item.get("slot_name", "-")))),
                    ft.DataCell(ft.Text(str(item.get("recoil_delta", 0)))),
                    ft.DataCell(ft.Text(str(item.get("ergonomics_delta", 0)))),
                ]
            )
            for item in parts
        ]
        self.page.update()

    def _open_detail(self, part_id: int) -> None:
        detail = self.service.get_part_detail(part_id)
        if detail is not None:
            open_part_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("총기 부품", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.type_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
