from __future__ import annotations

from typing import Any

from repositories.backpack_repository import BackpackRepository
from repositories.medical_repository import MedicalRepository
from repositories.rig_repository import RigRepository


class SupportItemService:
    """리그/백팩/의료품 조회 서비스."""

    def __init__(self) -> None:
        self.rig_repo = RigRepository()
        self.backpack_repo = BackpackRepository()
        self.medical_repo = MedicalRepository()

    def get_rigs(self) -> list[dict[str, Any]]:
        return self.rig_repo.find_all()

    def get_backpacks(self) -> list[dict[str, Any]]:
        return self.backpack_repo.find_all()

    def get_medicals(self) -> list[dict[str, Any]]:
        return self.medical_repo.find_all()

    def get_support_item_detail(self, category: str, item_id: int) -> dict[str, Any] | None:
        if category == "rig":
            return self.rig_repo.find_by_id(item_id)
        if category == "backpack":
            return self.backpack_repo.find_by_id(item_id)
        if category == "medical_item":
            return self.medical_repo.find_by_id(item_id)
        return None
