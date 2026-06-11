from __future__ import annotations

from typing import Callable

import flet as ft

from services.ammo_service import AmmoService
from services.armor_service import ArmorService
from services.helmet_service import HelmetService
from services.loadout_service import LoadoutService
from services.support_item_service import SupportItemService
from services.weapon_part_service import WeaponPartService
from services.weapon_service import WeaponService
from utils.helpers import safe_str, to_int_or_none


class LoadoutCreatePage:
    """세팅 생성 화면."""

    def __init__(
        self,
        page: ft.Page,
        weapon_service: WeaponService,
        part_service: WeaponPartService,
        ammo_service: AmmoService,
        armor_service: ArmorService,
        helmet_service: HelmetService,
        support_service: SupportItemService,
        loadout_service: LoadoutService,
        on_saved: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.weapon_service = weapon_service
        self.part_service = part_service
        self.ammo_service = ammo_service
        self.armor_service = armor_service
        self.helmet_service = helmet_service
        self.support_service = support_service
        self.loadout_service = loadout_service
        self.on_saved = on_saved

        self.name_field = ft.TextField(label="세팅 이름", width=300)
        self.memo_field = ft.TextField(label="메모", multiline=True, min_lines=2, max_lines=4, expand=True)
        self.weapon_dropdown = ft.Dropdown(label="총기", width=260)
        self.weapon_dropdown.on_change = self._on_weapon_change
        self.armor_dropdown = ft.Dropdown(label="방어구", width=240)
        self.helmet_dropdown = ft.Dropdown(label="헬멧", width=240)
        self.rig_dropdown = ft.Dropdown(label="리그", width=240)
        self.backpack_dropdown = ft.Dropdown(label="백팩", width=240)

        self.parts_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=140, spacing=4)

        self.ammo_rows: list[tuple[ft.Dropdown, ft.TextField]] = []
        self.medical_rows: list[tuple[ft.Dropdown, ft.TextField]] = []
        self.ammo_container = ft.Column(spacing=6)
        self.medical_container = ft.Column(spacing=6)

        self._prepare_options()
        self._append_ammo_row()
        self._append_medical_row()

    def _prepare_options(self) -> None:
        weapons = self.weapon_service.get_weapons()
        self.weapon_dropdown.options = [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in weapons
        ]

        armors = self.armor_service.get_armors()
        self.armor_dropdown.options = [ft.dropdown.Option("", "선택 안 함")] + [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in armors
        ]

        helmets = self.helmet_service.get_helmets()
        self.helmet_dropdown.options = [ft.dropdown.Option("", "선택 안 함")] + [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in helmets
        ]

        rigs = self.support_service.get_rigs()
        self.rig_dropdown.options = [ft.dropdown.Option("", "선택 안 함")] + [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in rigs
        ]

        backpacks = self.support_service.get_backpacks()
        self.backpack_dropdown.options = [ft.dropdown.Option("", "선택 안 함")] + [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in backpacks
        ]

    def _on_weapon_change(self, _: ft.ControlEvent) -> None:
        self.parts_column.controls.clear()
        weapon_id = to_int_or_none(self.weapon_dropdown.value)
        if weapon_id is None:
            self.page.update()
            return

        parts = self.part_service.get_parts_by_weapon(weapon_id)
        for item in parts:
            self.parts_column.controls.append(
                ft.Checkbox(label=f"{item['name']} ({item.get('slot_name', '-')})", data=item["id"])
            )
        self.page.update()

    def _append_ammo_row(self) -> None:
        dropdown = ft.Dropdown(label="탄약", width=260)
        dropdown.options = [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in self.ammo_service.get_ammos()
        ]
        qty = ft.TextField(label="수량", width=100, value="1")
        self.ammo_rows.append((dropdown, qty))
        self.ammo_container.controls.append(ft.Row([dropdown, qty]))

    def _append_medical_row(self) -> None:
        dropdown = ft.Dropdown(label="의료품", width=260)
        dropdown.options = [
            ft.dropdown.Option(str(item["id"]), item["name"]) for item in self.support_service.get_medicals()
        ]
        qty = ft.TextField(label="수량", width=100, value="1")
        self.medical_rows.append((dropdown, qty))
        self.medical_container.controls.append(ft.Row([dropdown, qty]))

    def _build_payload(self) -> dict:
        weapon_part_ids = [
            int(c.data)
            for c in self.parts_column.controls
            if isinstance(c, ft.Checkbox) and c.value
        ]

        ammo_items = []
        for dropdown, qty in self.ammo_rows:
            ammo_id = to_int_or_none(dropdown.value)
            quantity = to_int_or_none(qty.value)
            if ammo_id is not None:
                ammo_items.append({"ammo_id": ammo_id, "quantity": quantity or 0})

        medical_items = []
        for dropdown, qty in self.medical_rows:
            med_id = to_int_or_none(dropdown.value)
            quantity = to_int_or_none(qty.value)
            if med_id is not None:
                medical_items.append({"medical_item_id": med_id, "quantity": quantity or 0})

        return {
            "user_id": 1,
            "name": safe_str(self.name_field.value),
            "memo": safe_str(self.memo_field.value),
            "weapon_id": to_int_or_none(self.weapon_dropdown.value),
            "weapon_part_ids": weapon_part_ids,
            "ammo_items": ammo_items,
            "armor_id": to_int_or_none(self.armor_dropdown.value),
            "helmet_id": to_int_or_none(self.helmet_dropdown.value),
            "rig_id": to_int_or_none(self.rig_dropdown.value),
            "backpack_id": to_int_or_none(self.backpack_dropdown.value),
            "medical_items": medical_items,
        }

    def _save(self, _: ft.ControlEvent) -> None:
        success, message, _ = self.loadout_service.create_loadout(self._build_payload())
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        if success:
            self._reset(None)
            if self.on_saved is not None:
                self.on_saved()
        self.page.update()

    def _reset(self, _: ft.ControlEvent | None) -> None:
        self.name_field.value = ""
        self.memo_field.value = ""
        self.weapon_dropdown.value = None
        self.armor_dropdown.value = ""
        self.helmet_dropdown.value = ""
        self.rig_dropdown.value = ""
        self.backpack_dropdown.value = ""
        self.parts_column.controls.clear()

        self.ammo_rows.clear()
        self.medical_rows.clear()
        self.ammo_container.controls.clear()
        self.medical_container.controls.clear()
        self._append_ammo_row()
        self._append_medical_row()
        self.page.update()

    def build(self) -> ft.Control:
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("세팅 생성", size=24, weight=ft.FontWeight.BOLD),
                self.name_field,
                self.memo_field,
                self.weapon_dropdown,
                ft.Text("총기 부품(다중 선택)"),
                self.parts_column,
                ft.Row([
                    ft.Text("탄약"),
                    ft.TextButton("탄약 행 추가", on_click=lambda _: self._append_ammo_row() or self.page.update()),
                ]),
                self.ammo_container,
                ft.Row([self.armor_dropdown, self.helmet_dropdown]),
                ft.Row([self.rig_dropdown, self.backpack_dropdown]),
                ft.Row([
                    ft.Text("의료품"),
                    ft.TextButton("의료품 행 추가", on_click=lambda _: self._append_medical_row() or self.page.update()),
                ]),
                self.medical_container,
                ft.Row(
                    [
                        ft.ElevatedButton("저장", on_click=self._save),
                        ft.OutlinedButton("초기화", on_click=self._reset),
                    ]
                ),
            ],
        )
