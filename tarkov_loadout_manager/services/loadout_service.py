from __future__ import annotations

from typing import Any

from repositories.loadout_join_repository import LoadoutJoinRepository
from repositories.loadout_repository import LoadoutRepository
from utils.validators import validate_loadout_payload


class LoadoutService:
    """세팅 생성/조회/수정/삭제 핵심 서비스."""

    def __init__(self) -> None:
        self.repo = LoadoutRepository()
        self.join_repo = LoadoutJoinRepository()

    def create_loadout(self, payload: dict[str, Any]) -> tuple[bool, str, int | None]:
        """세팅을 새로 생성하고 결과 메시지를 반환한다."""
        try:
            is_valid, message = validate_loadout_payload(payload)
            if not is_valid:
                return False, message, None

            loadout_id = self.repo.save_loadout_base(
                user_id=int(payload["user_id"]),
                name=str(payload["name"]).strip(),
                memo=payload.get("memo"),
            )
            self.repo.save_loadout_components(loadout_id, payload)
            return True, "세팅이 저장되었습니다.", loadout_id
        except Exception as exc:
            return False, f"세팅 저장 중 오류가 발생했습니다: {exc}", None

    def get_loadout_list(self, user_id: int) -> list[dict[str, Any]]:
        return self.join_repo.find_all_loadouts_summary(user_id)

    def get_loadout_detail(self, loadout_id: int) -> dict[str, Any] | None:
        return self.join_repo.find_loadout_detail(loadout_id)

    def update_loadout(self, loadout_id: int, payload: dict[str, Any]) -> tuple[bool, str]:
        """세팅 수정 시 하위 데이터를 재삽입하는 방식으로 처리한다."""
        try:
            is_valid, message = validate_loadout_payload(payload)
            if not is_valid:
                return False, message

            self.repo.update_loadout_base(loadout_id, str(payload["name"]).strip(), payload.get("memo"))
            self.repo.clear_loadout_children(loadout_id)
            self.repo.save_loadout_components(loadout_id, payload)
            return True, "세팅이 수정되었습니다."
        except Exception as exc:
            return False, f"세팅 수정 중 오류가 발생했습니다: {exc}"

    def delete_loadout(self, loadout_id: int) -> tuple[bool, str]:
        try:
            self.repo.delete(loadout_id)
            return True, "세팅이 삭제되었습니다."
        except Exception as exc:
            return False, f"세팅 삭제 중 오류가 발생했습니다: {exc}"
