from __future__ import annotations

import flet as ft

from services.loadout_service import LoadoutService
from ui.loadout_detail_page import build_loadout_detail


class LoadoutListPage:
    """저장된 세팅 목록/상세 조회 + 수정/삭제 UI."""

    def __init__(self, page: ft.Page, service: LoadoutService, user_id: int = 1) -> None:
        self.page = page
        self.service = service
        self.user_id = user_id

        self.list_view = ft.ListView(expand=True, spacing=6)
        self.detail_container = ft.Container(expand=True, padding=12)
        self.refresh()

    def refresh(self) -> None:
        items = self.service.get_loadout_list(self.user_id)
        self.list_view.controls = [
            ft.ListTile(
                title=ft.Text(item["name"]),
                subtitle=ft.Text(f"{item.get('weapon_name', '-')}, {item.get('created_at', '-')}") ,
                on_click=lambda _, lid=item["id"]: self._show_detail(lid),
            )
            for item in items
        ]
        if not self.detail_container.content:
            self.detail_container.content = ft.Text("왼쪽에서 세팅을 선택하세요.")
        self.page.update()

    def _show_detail(self, loadout_id: int) -> None:
        detail = self.service.get_loadout_detail(loadout_id)
        if detail is None:
            self.detail_container.content = ft.Text("세팅 정보를 찾을 수 없습니다.")
            self.page.update()
            return

        self.detail_container.content = build_loadout_detail(
            detail,
            on_edit=lambda: self._open_edit_dialog(loadout_id, detail),
            on_delete=lambda: self._delete_loadout(loadout_id),
        )
        self.page.update()

    def _open_edit_dialog(self, loadout_id: int, detail: dict) -> None:
        header = detail["header"]
        name_field = ft.TextField(label="세팅 이름", value=str(header.get("name", "")), width=320)
        raid_purpose_field = ft.TextField(label="레이드 목적", value=str(header.get("raid_purpose", "")), width=320)
        memo_field = ft.TextField(label="메모", value=str(header.get("memo", "")), multiline=True, min_lines=2)

        dialog = ft.AlertDialog(
            title=ft.Text("세팅 수정"),
            content=ft.Container(width=420, content=ft.Column(tight=True, controls=[name_field, raid_purpose_field, memo_field])),
            actions=[
                ft.TextButton("취소", on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(
                    "저장",
                    on_click=lambda _: self._save_edit(
                        dialog,
                        loadout_id,
                        name_field.value or "",
                        raid_purpose_field.value or "",
                        memo_field.value or "",
                        detail,
                    ),
                ),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _save_edit(
        self,
        dialog: ft.AlertDialog,
        loadout_id: int,
        name: str,
        raid_purpose: str,
        memo: str,
        detail: dict,
    ) -> None:
        weapon = detail.get("weapon") or {}
        payload = {
            "user_id": int(detail["header"].get("user_id", self.user_id)),
            "name": name,
            "raid_purpose": raid_purpose,
            "memo": memo,
            "weapon_id": weapon.get("id"),
            "weapon_part_ids": [item["id"] for item in detail.get("weapon_parts", [])],
            "ammo_items": [
                {"ammo_id": item["id"], "quantity": int(item.get("quantity", 1))}
                for item in detail.get("ammo_items", [])
            ],
            "armor_id": (detail.get("armor") or {}).get("id"),
            "helmet_id": (detail.get("helmet") or {}).get("id"),
            "rig_id": (detail.get("rig") or {}).get("id"),
            "backpack_id": (detail.get("backpack") or {}).get("id"),
            "medical_items": [
                {"medical_item_id": item["id"], "quantity": int(item.get("quantity", 1))}
                for item in detail.get("medical_items", [])
            ],
            "support_items": [
                {
                    "support_item_id": item["id"],
                    "quantity": int(item.get("quantity", 1)),
                    "slot_label": item.get("slot_label"),
                }
                for item in detail.get("support_items", [])
                if item.get("item_type") not in {"rig", "backpack", "medical"}
            ],
        }
        success, message = self.service.update_loadout(loadout_id, payload)
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self._close_dialog(dialog)
        if success:
            self.refresh()
            self._show_detail(loadout_id)
        self.page.update()

    def _delete_loadout(self, loadout_id: int) -> None:
        success, message = self.service.delete_loadout(loadout_id)
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        if success:
            self.detail_container.content = ft.Text("세팅이 삭제되었습니다.")
            self.refresh()
        self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog) -> None:
        dialog.open = False
        self.page.update()

    def build(self) -> ft.Control:
        return ft.Column(
            expand=True,
            controls=[
                ft.Text("저장 세팅 조회", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(width=320, content=self.list_view),
                        ft.VerticalDivider(width=1),
                        self.detail_container,
                    ],
                ),
            ],
        )
