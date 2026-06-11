from __future__ import annotations

import flet as ft

from services.support_item_service import SupportItemService
from ui.support_item_detail_dialog import open_support_item_detail_dialog


class SupportItemPage:
    """보조 장비 탭 UI (리그/백팩/의료품)."""

    def __init__(self, page: ft.Page, service: SupportItemService) -> None:
        self.page = page
        self.service = service
        self.current_category = "rig"
        self.list_container = ft.Container(expand=True)

    def _build_list(self, category: str, label: str, items: list[dict]) -> ft.Control:
        return ft.ListView(
            expand=True,
            spacing=6,
            controls=[
                ft.ListTile(
                    title=ft.Text(item["name"]),
                    subtitle=ft.Text(str(item.get("description", ""))),
                    on_click=lambda _, c=category, iid=item["id"], l=label: self._open_detail(c, iid, l),
                )
                for item in items
            ],
        )

    def _open_detail(self, category: str, item_id: int, label: str) -> None:
        detail = self.service.get_support_item_detail(category, item_id)
        if detail is not None:
            open_support_item_detail_dialog(self.page, label, detail)

    def _render_category(self) -> None:
        """선택된 카테고리에 맞는 목록을 렌더링한다."""
        if self.current_category == "rig":
            self.list_container.content = self._build_list("rig", "리그", self.service.get_rigs())
        elif self.current_category == "backpack":
            self.list_container.content = self._build_list("backpack", "백팩", self.service.get_backpacks())
        else:
            self.list_container.content = self._build_list("medical_item", "의료품", self.service.get_medicals())

    def _on_category_change(self, e: ft.ControlEvent) -> None:
        selected = e.control.selected
        if not selected:
            return
        self.current_category = selected[0]
        self._render_category()
        self.page.update()

    def build(self) -> ft.Control:
        self._render_category()

        return ft.Column(
            expand=True,
            controls=[
                ft.Text("보조 장비", size=24, weight=ft.FontWeight.BOLD),
                ft.SegmentedButton(
                    segments=[
                        ft.Segment(value="rig", label="리그"),
                        ft.Segment(value="backpack", label="백팩"),
                        ft.Segment(value="medical_item", label="의료품"),
                    ],
                    selected=[self.current_category],
                    on_change=self._on_category_change,
                ),
                self.list_container,
            ],
        )
