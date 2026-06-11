from __future__ import annotations

import flet as ft

from services.ammo_service import AmmoService
from services.defense_gear_service import DefenseGearService
from services.loadout_service import LoadoutService
from services.support_item_service import SupportItemService
from services.weapon_part_service import WeaponPartService
from services.weapon_service import WeaponService
from ui.ammo_page import AmmoPage
from ui.defense_gear_page import DefenseGearPage
from ui.loadout_create_page import LoadoutCreatePage
from ui.loadout_list_page import LoadoutListPage
from ui.part_page import PartPage
from ui.support_item_page import SupportItemPage
from ui.weapon_page import WeaponPage


class MainLayout:
    """좌측 사이드바 + 우측 메인 콘텐츠 레이아웃."""

    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.weapon_service = WeaponService()
        self.part_service = WeaponPartService()
        self.ammo_service = AmmoService()
        self.defense_gear_service = DefenseGearService()
        self.support_service = SupportItemService()
        self.loadout_service = LoadoutService()

        self.loadout_list_page = LoadoutListPage(page, self.loadout_service)

        self.pages = {
            "총기 조회": WeaponPage(page, self.weapon_service),
            "총기 부품 조회": PartPage(page, self.part_service),
            "탄약 조회": AmmoPage(page, self.ammo_service),
            "방어 장비 조회": DefenseGearPage(page, self.defense_gear_service),
            "보조 장비 조회": SupportItemPage(page, self.support_service),
            "세팅 생성": LoadoutCreatePage(
                page,
                self.weapon_service,
                self.part_service,
                self.ammo_service,
                self.defense_gear_service,
                self.support_service,
                self.loadout_service,
                on_saved=self.loadout_list_page.refresh,
            ),
            "저장 세팅 조회": self.loadout_list_page,
        }

        self.menu_labels = list(self.pages.keys())
        self.content_container = ft.Container(expand=True, padding=12)

    def _change_page(self, index: int) -> None:
        key = self.menu_labels[index]
        self.content_container.content = self.pages[key].build()
        self.page.update()

    def build(self) -> ft.Control:
        nav = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=120,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.CHEVRON_RIGHT, label=label)
                for label in self.menu_labels
            ],
            on_change=lambda e: self._change_page(int(e.control.selected_index)),
        )

        self.content_container.content = self.pages[self.menu_labels[0]].build()

        return ft.Row(
            expand=True,
            controls=[
                ft.Container(width=220, bgcolor="#f2f2f2", content=nav),
                ft.VerticalDivider(width=1),
                self.content_container,
            ],
        )
