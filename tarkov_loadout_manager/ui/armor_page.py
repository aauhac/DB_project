from __future__ import annotations

import flet as ft

from services.armor_service import ArmorService
from ui.armor_detail_dialog import open_armor_detail_dialog


class ArmorPage:
    """방어구 목록/필터 UI."""

    def __init__(self, page: ft.Page, service: ArmorService) -> None:
        self.page = page
        self.service = service
        self.class_dropdown = ft.Dropdown(label="방어 등급", width=180)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("이름")),
                ft.DataColumn(ft.Text("등급")),
                ft.DataColumn(ft.Text("내구도")),
            ],
            rows=[],
        )
        self.class_dropdown.on_change = lambda _: self.refresh()
        self._load_classes()
        self.refresh()

    def _load_classes(self) -> None:
        self.class_dropdown.options = [ft.dropdown.Option("", "전체")]
        self.class_dropdown.options.extend(
            [ft.dropdown.Option(str(c), str(c)) for c in self.service.get_classes()]
        )

    def refresh(self) -> None:
        class_value = int(self.class_dropdown.value) if self.class_dropdown.value else None
        armors = self.service.get_armors(class_value)
        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item["id"]))),
                    ft.DataCell(
                        ft.TextButton(
                            item["name"],
                            on_click=lambda _, aid=item["id"]: self._open_detail(aid),
                        )
                    ),
                    ft.DataCell(ft.Text(str(item["armor_class"]))),
                    ft.DataCell(ft.Text(str(item["durability"]))),
                ]
            )
            for item in armors
        ]
        self.page.update()

    def _open_detail(self, armor_id: int) -> None:
        detail = self.service.get_armor_detail(armor_id)
        if detail is not None:
            open_armor_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("방어구", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.class_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
