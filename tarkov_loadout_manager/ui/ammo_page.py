from __future__ import annotations

import flet as ft

from services.ammo_service import AmmoService
from ui.ammo_detail_dialog import open_ammo_detail_dialog


class AmmoPage:
    """탄약 목록/필터 UI."""

    def __init__(self, page: ft.Page, service: AmmoService) -> None:
        self.page = page
        self.service = service
        self.caliber_dropdown = ft.Dropdown(label="구경", width=220)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("이름")),
                ft.DataColumn(ft.Text("구경")),
                ft.DataColumn(ft.Text("데미지")),
                ft.DataColumn(ft.Text("관통")),
            ],
            rows=[],
        )
        self.caliber_dropdown.on_change = lambda _: self.refresh()
        self._load_calibers()
        self.refresh()

    def _load_calibers(self) -> None:
        self.caliber_dropdown.options = [ft.dropdown.Option("", "전체")]
        self.caliber_dropdown.options.extend(
            [ft.dropdown.Option(caliber, caliber) for caliber in self.service.get_calibers()]
        )

    def refresh(self) -> None:
        ammos = self.service.get_ammos(self.caliber_dropdown.value or "")
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
                    ft.DataCell(ft.Text(str(item["caliber"]))),
                    ft.DataCell(ft.Text(str(item["damage"]))),
                    ft.DataCell(ft.Text(str(item["penetration"]))),
                ]
            )
            for item in ammos
        ]
        self.page.update()

    def _open_detail(self, ammo_id: int) -> None:
        detail = self.service.get_ammo_detail(ammo_id)
        if detail is not None:
            open_ammo_detail_dialog(self.page, detail)

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text("탄약", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.caliber_dropdown]),
                ft.Container(content=ft.Row([self.table], scroll=ft.ScrollMode.AUTO), expand=True),
            ],
            expand=True,
        )
