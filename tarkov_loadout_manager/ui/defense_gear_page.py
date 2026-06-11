from __future__ import annotations

import flet as ft

from services.defense_gear_service import DefenseGearService
from ui.defense_gear_detail_dialog import open_defense_gear_detail_dialog


class DefenseGearPage:
    """방어 장비(defense_gear) 목록/필터 UI."""

    def __init__(self, page: ft.Page, service: DefenseGearService) -> None:
        self.page = page
        self.service = service
        self.gear_type_selector = ft.SegmentedButton(
            segments=[
                ft.Segment(value="all", label="전체"),
                ft.Segment(value="armor", label="방어구"),
                ft.Segment(value="helmet", label="헬멧"),
            ],
            selected=["all"],
        )
        self.class_dropdown = ft.Dropdown(label="방어 등급", width=180)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("이름")),
                ft.DataColumn(ft.Text("구분")),
                ft.DataColumn(ft.Text("등급")),
                ft.DataColumn(ft.Text("내구도")),
            ],
            rows=[],
        )
        self.gear_type_selector.on_change = lambda _: self._on_gear_type_change()
        self.class_dropdown.on_change = lambda _: self.refresh()
        self._load_classes()
        self.refresh()

    def _selected_gear_type(self) -> str | None:
        selected = self.gear_type_selector.selected
        if not selected or selected[0] == "all":
            return None
        return str(selected[0])

    def _on_gear_type_change(self) -> None:
        self._load_classes()
        self.refresh()

    def _load_classes(self) -> None:
        gear_type = self._selected_gear_type()
        self.class_dropdown.options = [ft.dropdown.Option("", "전체")]
        self.class_dropdown.options.extend(
            [ft.dropdown.Option(str(c), str(c)) for c in self.service.get_classes(gear_type)]
        )
        self.class_dropdown.value = ""

    def refresh(self) -> None:
        gear_type = self._selected_gear_type()
        class_value = int(self.class_dropdown.value) if self.class_dropdown.value else None
        armors = self.service.get_armors(class_value, gear_type)
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
                    ft.DataCell(ft.Text(str(item.get("gear_type", "-")))),
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
            open_defense_gear_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("방어 장비 조회", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.gear_type_selector]),
                ft.Row([self.class_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
