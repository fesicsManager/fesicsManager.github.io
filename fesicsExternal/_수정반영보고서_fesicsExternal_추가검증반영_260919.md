# fesicsExternal 추가 검증 반영 수정 보고서

- 작성일: 2026-09-19
- 대상 위치: Google Drive `Misodle Software/fesicsExternal`
- 반영 기준 보고서
  - `_추가검증보고서_fesicsExternal_260914_1차자동검증.md`
  - `_상세검증_fesicsExternal_fesicsLabs_260914.md`
  - `_상세검증_fesicsExternal_대학38개_260914.md`
  - `_상세검증_fesicsExternal_fesicsMathLabs_260914.md`
  - `_상세검증_fesicsExternal_zerolabMathHigh_260914.md`
  - `_중간진행보고서_fesicsExternal_예전405개재검증_260915.md`
- 수정 방식: 원본 HTML 직접 수정(UTF-8, BOM 없음 유지). 수정 후 1,008개 전체 인라인 JavaScript 구문·중복 id·고정 DOM 참조·viewport·@media 자동 검사 재통과.

## 1. 오류 18건 — 모두 수정

| # | 파일 | 수정 내용 |
|---|---|---|
| 1 | `zerolabMathHigh/hs_c1_12_cubic_root_count…` | "실근은 1개 또는 3개"를 중복도 포함 기준으로 한정. 서로 다른 실근은 1·2·3개 가능함을 원리·오해·예시에 추가. 표·읽기값에 `(중복 포함)` 명시. 기록 분석 문구 정정 |
| 2 | `zerolabMathHigh/hs_calc_55_increase_extremum…` | "f′=0은 필요조건일 뿐"에 미분 가능·내부점 조건(페르마 정리) 추가, 뾰족점 예외 명시 |
| 3 | `zerolabMathHigh/hs_stat_64_conditional_probability…` | 조건부확률 정의에 `P(A)>0`, 베이즈 공식에 `P(B)>0`, 독립 판정에 조건 추가 |
| 4 | `fesicsMathLabs/hm_inflection_lab…` | "f″(a)=0은 변곡점의 필요조건" 제목·본문·정리 문구를 볼록성 변화 기준으로 수정, `x^(1/3)` 반례 추가 |
| 5 | `fesicsMathLabs/hp_conditional_probability_lab…` | 곱셈정리 "항상 성립" → `P(A)>0`일 때, 독립 조건에 `P(B)>0` 추가 |
| 6 | `fesicsMathLabs/index.html` | 검색 입력 `#q`에 `aria-label="실험 검색"` 추가 |
| 7 | `univGenBio/genbio_lab11_antibiotic…` | MRSA "β-락탐 전부" → "대부분의 β-락탐", 항-MRSA 세팔로스포린 예외와 CLSI/EUCAST 판본 의존성 표시 |
| 8 | `univGenBio/genbio_lab06_mendel_chisquare…` | "가설 채택" → "귀무가설을 기각하지 못함" |
| 9 | `univMechanics/cm_sim14_spinning_top…` | 유효 퍼텐셜 발산을 `p_φ ≠ ±p_ψ`인 일반적인 경우로 한정, 잠자는 팽이 예외 추가 |
| 10 | `univMechanics/cm_sim10_rutherford…` | "힘이 실제로 0" → "빠르게 작아져 무시 가능(정확히 0은 아님)" 2곳 |
| 11 | `univEM/univ_em_10_biot_savart…` | 앙페르 법칙 "항상" → 정상 전류 조건으로 한정, 앙페르–맥스웰 일반식 병기 |
| 12 | `fesicsLabs/titration_buffer_cr…` | `add * 0` 버그 수정. 강산·순수한 물 모두 넣은 NaOH 몰수와 늘어난 부피를 반영해 pH 계산. 가정(1 L, 0.1 M NaOH 첨가)을 안내문에 명시 |
| 13 | `fesicsLabs/galvanic_cell_cr…` | `n = max(...)` → 두 반쪽 반응 전자 수의 최소공배수. Q에 반응식 계수만큼 거듭제곱 적용. 결과에 전자 수와 계수 표시 |
| 14 | `fesicsLabs/geologic_time_fossil…` | 검증 결과 기존 코드가 이미 교집합(Ma 기준 min(시작)·max(끝))을 계산하고 있어 로직 변경 없음. 의도를 주석으로 명시하고 빈 교집합 플래그 추가 |
| 15 | `fesicsLabs/phase_diagram_me…` | 화면·안내문에 "정성적 근사 모형(삼중점·끓는점·임계점만 실측)" 상시 표시. 그려지는 승화 곡선을 상태 판정과 같은 식으로 통일(기존 ×0.55 임의 배수 제거) |
| 16 | `fesicsLabs/solar_planets_ps…` | 위성 수에 기준 시점(2024년 초 확인 위성 수)·출처(NASA/IAU)·갱신 필요 안내 추가. "모두 실제 관측값" 문구 수정 |
| 17 | `fesicsLabs/planet_atmosphere_pu…` | 목성을 1기압 기준면 온도로 구분(gh 0→55, 내부열 기여 명시), 온실 효과가 행성별 관측 차이값이며 덧셈 상수가 아님을 표시. 라벨 "실제 표면 온도"를 기체 행성에서 "관측 온도(1기압면)"로 변경 |
| 18 | `fesicsLabs/hubble_law_earth…` | 은하를 z < 0.15 범위(최대 570 Mpc)로 제한(바다뱀자리 1,200 Mpc 제거, 페르세우스·머리털자리 추가). 그래프 축 0~700 Mpc / 0~50,000 km/s. 스펙트럼 표시 범위 380~460 nm로 확장(기존 420 nm까지라 z>0.07 은하의 흡수선이 화면 밖으로 나가던 문제 함께 해결). `v≈cz` 적용 범위 안내 |

## 2. 개선 권고 — 반영

- `fesicsLabs` 36개(보고서 표 기준): 장면 아래 안내문(`<p class="note">`)에 조건·가정·출처·모형 한계 문장 추가. `buoyancy_dyn_hs3_MechEnergy.html`은 완전히 잠긴 경우와 일부 잠긴 평형 상태의 부력을 코드에서 구분해 표시하도록 수정. `superconductor…`는 임계 자기장·임계 전류 조건 추가.
- 대학 17개: `univGenBio` 7개(Km 해석 조건, 감자 압력퍼텐셜, 모형값 표시, 로지스틱 한계, 전기영동 유효 범위, √(2Dt) 특성 길이, PFI·최대심박 출처·개인차), `univMechanics` 5개(점질량·무마찰 조건, 무리수 비 조건, 적분법·간격 표시 — 실제 코드가 반음해 오일러·dt 0.001 s임을 확인해 기재, 비구속계 넓이 산정, 푸앵카레 판정 한계), `univEM` 5개(2D 회전과 3D 스토크스 법선, "세 가지뿐" 완화, 표면 전하 조건, 반자성 기작·히스테리시스 임의 매개변수, 좋은 도체 근사).
- `fesicsMathLabs` 7개, `zerolabMathHigh` 6개: 정사영 각 범위, i.i.d.·유한모집단수정, 동전 24.6 %, 강수확률 보정 해석, 단순 다각형 외각, 정규분포 표준화 표현, 점근선 제목 한정, 신뢰구간 가정, 사인 주기 `2π/|b|`, 유리함수 `c≠0, ad−bc≠0`, 연속성 수정, 목걸이 조건, 실수 지수 범위.

## 3. 접근성

- 1차 자동검증의 `zerolabMathHigh` 14개 파일은 라디오 입력이 `<label><input …>선택지</label>` 구조로 이미 접근성 이름을 가지고 있어 수정 대상이 아님(상세검증 보고서 판정과 일치). 실제 누락은 `fesicsMathLabs/index.html` 1건이며 수정 완료.
- 보고서에 없던 신규 폴더 `elem56Tech`(33), `milddle1Tech`(8), `milddle2Tech`(8), `milddle3Tech`(10), `highTechHome`(40) — 2026-09-15 추가, 총 99개 — 에서 `<label>`이 `for` 없이 입력 앞에만 놓인 경우 419건을 발견해 `for="id"`로 연결. 이 99개는 아직 내용 검증 보고서가 없다.

## 4. 외부 의존성

- `univMechanics` 14개: MathJax CDN 로드 실패 시(오프라인·학교망 차단) 상단에 안내 띠를 표시하고 수식은 TeX 원문으로 남기는 폴백 스크립트 추가. 로컬 번들 동봉은 하지 않았다(약 1 MB 이상 파일 추가가 필요하므로 별도 결정 필요).

## 5. 예전 405개 재검증 — 자동 검사 완료, 내용 전수 재판정은 미완료

- 기존 50개 폴더 405개(+Tech 99개) 자동 검사: JavaScript 구문 오류 0, 중복 id 0, 존재하지 않는 고정 DOM 참조 0, viewport·@media 누락 0.
- 2026-09-12 보고서의 기술 오류(`01_animal_physics_lab`의 `camelAddBtn` 등 3개 참조, `milddle1Chem`의 `zlNudge` 참조·중복 id·중복 스크립트)는 모두 해소된 상태.
- 2026-09-12 보고서에서 접근성 이름이 없다고 한 초·중 입력 요소도 현재는 모두 연결되어 있음.
- 표본 대조(달걀 부화 온도 범위, 소금물 농도 기준, 행성 위성 수·출처, 전지 밝기 등)에서 09-14 수정본은 지적 사항을 반영한 것으로 확인.
- 405개 전체의 과학 내용·수식·수치 전수 재판정과 "09-12 오류 83개 항목별 수정 확인 목록"은 이번 작업에 포함하지 않았다. 이어서 진행하려면 폴더 묶음별(초등 → 중등 → 고등 → 대학)로 `_재검증보고서_fesicsExternal_기존405개_…md` 형태로 작성하는 것이 적절하다.

## 6. 후속 권고

1. 실제 브라우저(360 px, 키보드, 연속 클릭, 탭 전환 후 애니메이션)에서 이번에 코드가 바뀐 5개 실험 확인: `titration_buffer`, `galvanic_cell`, `phase_diagram`, `planet_atmosphere`, `hubble_law`, `buoyancy`.
2. `solar_planets`의 위성 수를 최신 NASA/IAU 값으로 갱신(현재 값은 2024년 초 기준으로 표기).
3. Tech 폴더 99개 내용 검증.
4. 예전 405개 내용 전수 재판정.
