from __future__ import annotations

from typing import Any

from repositories.ammo_repository import AmmoRepository


class AmmoService:
    """탄약 조회 관련 비즈니스 로직."""

    def __init__(self) -> None:
        self.repo = AmmoRepository()

    def get_ammos(self, caliber: str = "") -> list[dict[str, Any]]:
        if caliber.strip():
            return self.repo.find_by_caliber(caliber)
        return self.repo.find_all()

    def get_ammo_detail(self, ammo_id: int) -> dict[str, Any] | None:
        return self.repo.find_by_id(ammo_id)

    def get_calibers(self) -> list[str]:
        rows = self.repo.fetch_all("SELECT DISTINCT caliber FROM ammo ORDER BY caliber")
        return [str(row["caliber"]) for row in rows]
