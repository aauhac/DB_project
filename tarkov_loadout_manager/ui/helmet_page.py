from __future__ import annotations

import flet as ft

from services.helmet_service import HelmetService
from ui.helmet_detail_dialog import open_helmet_detail_dialog


class HelmetPage:
    """헬멧 목록/필터 UI."""

    def __init__(self, page: ft.Page, service: HelmetService) -> None:
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
        helmets = self.service.get_helmets(class_value)
        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item["id"]))),
                    ft.DataCell(
                        ft.TextButton(
                            item["name"],
                            on_click=lambda _, hid=item["id"]: self._open_detail(hid),
                        )
                    ),
                    ft.DataCell(ft.Text(str(item["armor_class"]))),
                    ft.DataCell(ft.Text(str(item["durability"]))),
                ]
            )
            for item in helmets
        ]
        self.page.update()

    def _open_detail(self, helmet_id: int) -> None:
        detail = self.service.get_helmet_detail(helmet_id)
        if detail is not None:
            open_helmet_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("헬멧", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.class_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
