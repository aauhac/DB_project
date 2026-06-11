from __future__ import annotations

import flet as ft

from services.weapon_service import WeaponService
from ui.weapon_detail_dialog import open_weapon_detail_dialog


class WeaponPage:
    """총기 목록/검색/유형 필터 UI."""

    def __init__(self, page: ft.Page, service: WeaponService) -> None:
        self.page = page
        self.service = service
        self.search_field = ft.TextField(label="총기 검색", expand=True)
        self.type_dropdown = ft.Dropdown(label="총기 유형", width=180)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("이름")),
                ft.DataColumn(ft.Text("구경")),
                ft.DataColumn(ft.Text("반동")),
                ft.DataColumn(ft.Text("에르고")),
            ],
            rows=[],
        )

        self.search_field.on_change = lambda _: self.refresh()
        self.type_dropdown.on_change = lambda _: self.refresh()
        self._load_type_options()
        self.refresh()

    def _load_type_options(self) -> None:
        types = self.service.get_weapon_types()
        self.type_dropdown.options = [ft.dropdown.Option("", "전체")]
        self.type_dropdown.options.extend(
            [ft.dropdown.Option(str(item["name"]), str(item["name"])) for item in types]
        )

    def refresh(self) -> None:
        type_value = self.type_dropdown.value
        type_name = type_value if type_value else None
        weapons = self.service.get_weapons(
            name_keyword=self.search_field.value or "",
            weapon_type=type_name,
        )

        rows: list[ft.DataRow] = []
        for weapon in weapons:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(weapon["id"]))),
                        ft.DataCell(
                            ft.TextButton(
                                weapon["name"],
                                on_click=lambda _, wid=weapon["id"]: self._open_detail(wid),
                            )
                        ),
                        ft.DataCell(ft.Text(str(weapon["caliber"]))),
                        ft.DataCell(ft.Text(str(weapon.get("recoil", "-")))),
                        ft.DataCell(ft.Text(str(weapon.get("ergonomics", "-")))),
                    ]
                )
            )
        self.table.rows = rows
        self.page.update()

    def _open_detail(self, weapon_id: int) -> None:
        detail = self.service.get_weapon_detail(weapon_id)
        if detail is not None:
            open_weapon_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("총기", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.search_field, self.type_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
