# Escape from Tarkov 장비 세팅 관리 시스템

## 프로젝트 개요
Python + DuckDB + Flet 기반의 대학 데이터베이스 텀프로젝트 예제입니다.
게임 장비 데이터를 저장하고, GUI에서 조회/세팅 생성/저장/조회/수정/삭제 기능을 제공합니다.

## 사용 기술
- Python 3.x
- DuckDB
- Flet
- uv (실행 도구)

## 폴더 구조
```text
tarkov_loadout_manager/
  app.py
  requirements.txt
  README.md
  db/
    database.py
    schema.py
    seed.py
  repositories/
    base_repository.py
    weapon_repository.py
    weapon_part_repository.py
    ammo_repository.py
    loadout_repository.py
    loadout_join_repository.py
  services/
    weapon_service.py
    weapon_part_service.py
    ammo_service.py
    defense_gear_service.py
    support_item_service.py
    loadout_service.py
  ui/
    main_layout.py
    weapon_page.py
    weapon_detail_dialog.py
    part_page.py
    part_detail_dialog.py
    ammo_page.py
    ammo_detail_dialog.py
    defense_gear_page.py
    defense_gear_detail_dialog.py
    support_item_page.py
    support_item_detail_dialog.py
    loadout_create_page.py
    loadout_list_page.py
    loadout_detail_page.py
  utils/
    validators.py
    helpers.py
```

## 실행 방법
1. 가상환경 활성화
```powershell
.\.venv\Scripts\Activate
```
2. 의존성 설치
```powershell
pip install -r requirements.txt
```
3. 앱 실행
```powershell
cd tarkov_loadout_manager
python app.py
```
또는
```powershell
uv run flet run app.py
```

## DB 초기화 방법
- 앱 실행 시 `initialize_database(seed=True)`가 호출되어 테이블 생성 + 시드 삽입을 수행합니다.
- DB 파일명: `tarkov_loadout.duckdb`

## 주요 기능
- 총기/부품/탄약/방어 장비/보조 장비 목록 및 상세 조회
- 세팅 생성 및 저장
- 저장 세팅 목록 조회
- 저장 세팅 상세 조회 (Join 결과 통합)
- 저장 세팅 수정
- 저장 세팅 삭제

## 주요 테이블 설명
- `app_user`: 사용자 정보
- `weapon`: 총기 마스터 (weapon_category 기반)
- `weapon_part`: 총기 부품 마스터 (weapon_id FK)
- `ammo`: 탄약 마스터
- `defense_gear`: 방어 장비 통합 마스터 (gear_type = armor/helmet)
- `support_item`: 보조 장비 통합 마스터 (item_type = rig/backpack/medical)
- `loadout`: 세팅 헤더
- `loadout_item`: 세팅 상세 (item_category = weapon/weapon_part/ammo/defense_gear/support_item)

## JOIN 기능 설명
1. 총기 상세 조회
- `weapon` + `weapon_part`

2. 총기 부품 조회
- `weapon_part` (weapon_id 기준)

3. 세팅 상세 조회
- `loadout` + `app_user` + `loadout_item`
- `loadout_item.item_category`에 따라 `weapon`, `weapon_part`, `ammo`, `defense_gear`, `support_item` 조회

## 향후 개선점
- 세팅 수정 화면에서 모든 장비를 재선택할 수 있도록 폼 확장
- 이미지 파일 리소스 번들링
- 사용자 로그인/권한 분리
- 테스트 코드(Pytest) 추가
