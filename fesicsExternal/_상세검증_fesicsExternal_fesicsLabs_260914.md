# fesicsExternal 상세 검증 1 — fesicsLabs

- 검증일: 2026-09-14
- 대상: `fesicsExternal/fesicsLabs`
- 범위: HTML 195개(색인 1개, 실험 194개)
- 방식: 전체 소스 정적 검사 + 수식·계산 코드·화면 설명 대조
- 원본 변경: 없음

## 요약

| 판정 | 건수 | 의미 |
|---|---:|---|
| 오류 | 7 | 계산 결과 또는 핵심 설명을 우선 수정 |
| 개선 필요 | 34 | 조건·가정·출처·모형 한계를 보완 |
| 양호 | 154 | 이번 검사에서 중대한 문제를 찾지 못함 |

기술 구조는 195개 모두 JavaScript 구문, 중복 ID, 고정 DOM 참조, 반응형 CSS 검사에서 통과했다. 아래 판정은 기술 검사만이 아니라 화면 설명과 계산 코드의 일치 여부를 추가로 확인한 결과다.

## 오류 7개

### 1. `titration_buffer_cr_hs3_ChemReaction_Ep03_Ep05.html`

- 완충 비교의 강산 코드가 `0.1 + add * 0 + 0.1` 형태여서 NaOH 첨가량을 무시한다.
- 강산 pH가 첨가량에 따라 중화되지 않고 사실상 고정된다.
- 순수한 물도 첨가 뒤 전체 부피와 남은 OH⁻ 농도를 반영해야 한다.

### 2. `galvanic_cell_cr_hs3_ChemReaction_Ep08.html`

- 서로 다른 전자 수의 반쪽 반응을 조합하면서 `n = max(...)`를 사용한다.
- 반응지수 Q도 농도를 항상 1제곱으로 처리한다.
- Zn/Ag 전지처럼 `Q=[Zn²⁺]/[Ag⁺]²`가 필요한 경우 농도 효과와 ΔG가 틀어진다.
- 반쪽 반응 전자 수의 최소공배수로 전체 반응식, n, Q를 구성해야 한다.

### 3. `geologic_time_fossil_earth_hs2_EarthSci1_Ep09.html`

- 같은 층에서 여러 표준화석이 나올 때 연대 범위는 각 생존 범위의 교집합이어야 한다.
- 시작 시점의 최댓값과 끝 시점의 최솟값을 사용해야 하며, 합집합 범위로 넓히면 연대를 지나치게 넓게 판정한다.

### 4. `phase_diagram_me_hs3_MatterEnergy_Ep03.html`

- 삼중점·임계점 사이 상경계를 임의 곡선으로 만들고 실제 상평형도처럼 상태를 판정한다.
- 물과 CO₂의 증기압·융해·승화 경계에는 검증된 물성식이나 데이터 표가 필요하다.
- 유지하려면 화면 전체에 `정성적 가상 모형`임을 표시해야 한다.

### 5. `solar_planets_ps_hs3_PlanetUniverse_Ep03.html`

- 화면은 “모두 실제 관측값”이라고 하지만 위성 수가 목성 95, 토성 146, 천왕성 28로 고정돼 있다.
- 시점에 따라 바뀌는 수치이므로 기준일과 출처를 붙이고 최신 자료로 갱신해야 한다.

### 6. `planet_atmosphere_pu_hs3_PlanetUniverse_Ep05.html`

- 고정 온실효과 값을 복사평형온도에 더해 `실제 표면 온도`로 제시한다.
- 기체행성에도 고체 표면과 같은 개념을 적용한다.
- 기체행성은 구름꼭대기 또는 기준 압력면 온도를 구분하고, 온실효과를 단순 덧셈 상수로 일반화하지 않아야 한다.

### 7. `hubble_law_earth_hs2_EarthSci1_Ep17.html`

- 그래프 범위가 1,400 Mpc인데 전 범위에서 `z=H₀d/c`, `v≈cz`를 사용한다.
- 끝점은 낮은 적색편이 근사 범위를 벗어나므로 정밀 관측처럼 제시하기 어렵다.
- 거리를 낮은 z 범위로 제한하거나 우주론적 적색편이–거리 관계를 적용해야 한다.

## 개선 필요 34개

### 물리학·역학과 에너지

| 파일 | 개선 내용 |
|---|---|
| `magnetic_materials_hs2_Physics1_Ep10.html` | 축상 자기장과 단일 감수율로 저울 힘을 계산한 이상화 조건 표시 |
| `photoelectric_effect_hs2_Physics1_Ep15.html` | 전자 에너지 분포를 균일, 광전류를 직선으로 둔 모형임은 잘 밝혔으나 적용 범위를 결과 가까이에 반복 표시 |
| `pn_diode_hs2_Physics1_Ep17.html` | 온도·직렬저항·이상 다이오드 조건 명시 |
| `heat_engine_dyn_hs3_MechEnergy_Ep10.html` | 기관 효율을 카르노 효율의 고정 비율로 둔 값의 근거 또는 가상값 표시 |
| `escape_velocity_dyn_hs3_MechEnergy_Ep05.html` | 원궤도·대기저항 및 중력손실 무시 조건을 결과표에도 표시 |
| `buoyancy_dyn_hs3_MechEnergy.html` | 물체가 완전히 잠긴 경우와 일부 잠긴 경우를 구분 |

### 화학·물질과 에너지·화학 반응

| 파일 | 개선 내용 |
|---|---|
| `molecular_shape_chem_hs2_Chem1_Ep06-07.html` | 극성분자가 전기장에 모두 완전히 정렬하는 그림에 열운동과 통계적 배향 설명 추가 |
| `ideal_gas_law_me_hs3_MatterEnergy_Ep01.html` | 반데르발스식을 `실제 기체의 압력` 자체로 단정하지 말고 근사 상태방정식으로 표시 |
| `intermolecular_force_me_hs3_MatterEnergy_Ep03.html` | 녹는점·끓는점 바로 위아래와 상경계에서의 두 상 공존을 구분 |
| `liquid_property_me_hs3_MatterEnergy_Ep05.html` | 20℃ 물성값의 출처, 관 반지름·층류·뉴턴 유체 조건 표시 |
| `lattice_energy_me_hs3_MatterEnergy_Ep04.html` | 각 열화학 값의 기준 상태와 데이터 출처 표시 |
| `k_temperature_cr_hs3_Chem1_Ep11.html` | ΔH°가 온도 범위에서 일정하다는 반트호프 적분 가정 표시 |
| `solubility_ksp_cr_hs3_ChemReaction.html` | 활동도 대신 농도를 쓰는 근사와 25℃ 조건을 결과에 유지 |
| `battery_cr_hs3_ChemReaction_Ep10.html` | 에너지 밀도·수명을 단일 실제값이 아닌 범위·대표값으로 표시 |
| `corrosion_cr_hs3_IntegSci2_Change_Ep05.html` | 상대 모형값 표시는 적절하나 온도·염도·산소·표면 상태에 따른 차이 보완 |

### 생명과학·세포와 물질대사·유전

| 파일 | 개선 내용 |
|---|---|
| `digestive_enzyme_bio_hs2_Bio1_Ep03.html` | 효소별 pH·온도 곡선을 동일하게 고정하지 말고 대표값·실험조건 표시 |
| `immune_vaccine_bio_hs2_Bio1_Ep12_Ep14.html` | 상대값 모형 표시는 적절하나 선천·체액성·세포성 면역을 단일 순서로 읽히지 않게 보완 |
| `meiosis_gamete_diversity_bio_hs2_Bio1_Ep16.html` | 교차가 한 위치에서만 일어나는 단순 모형임을 명시 |
| `phylogenetic_tree_bio_hs2_Bio1_Ep19.html` | 공유 형질 개수만으로 만든 군집이 실제 계통 추론을 대신하지 않음을 표시 |
| `enzyme_kinetics_cm_hs3_CellMetab_Ep08-09.html` | 단일 기질 미카엘리스–멘텐 조건과 pH·온도 곡선의 가상 매개변수 표시 |
| `gene_linkage_gn_hs3_Genetics.html` | 1%≈1 cM은 짧은 거리에서의 근사이며 재조합률 상한은 50%임을 추가 |

### 지구과학·지구시스템·행성우주

| 파일 | 개선 내용 |
|---|---|
| `thermohaline_earth_hs2_EarthSci1_Ep02.html` | 단일 밀도 임계값으로 심층수 형성을 결정하는 모형 한계 표시 |
| `midlatitude_cyclone_earth_hs2_EarthSci1_Ep03.html` | 전선 통과 날씨를 고정 순서로 일반화하지 않도록 사례 조건 표시 |
| `typhoon_wind_earth_hs2_EarthSci1_Ep04.html` | 이상화한 대칭 태풍장과 실제 비대칭·지형·이동 효과 구분 |
| `radiometric_age_earth_hs2_EarthSci1_Ep08.html` | 딸원소 초기량 0·폐쇄계 가정 표시 |
| `stellar_evolution_earth_hs2_EarthSci1_Ep15.html` | 질량별 단일 진화 경로에 금속함량·질량손실·쌍성 효과 안내 |
| `ekman_transport_gs_hs3_EarthSystem_Ep06.html` | 표층 45°는 이상적 정상상태 모형이며 실제 각도는 혼합·마찰에 따라 달라짐을 표시 |
| `precipitation_gs_hs3_EarthSystem_Ep12.html` | 습윤단열감률을 0.5℃/100m로 고정한 근사와 온도·수증기량 의존성 표시 |
| `global_circulation_gs_hs3_EarthSystem_Ep15.html` | 자전을 끈 1세포 모형과 실제 대기 대순환의 계절·대륙 효과 구분 |
| `carbon_cycle_gs_hs3_EarthSystem_Ep02.html` | IPCC 자료의 보고서·연도와 저장량·흐름 불확실성 표시 |
| `star_cluster_pu_hs3_PlanetUniverse_Ep11.html` | 실제 관측값의 대상 성단·자료 출처 및 금속함량·쌍성에 따른 전향점 오차 표시 |
| `small_bodies_pu_hs3_PlanetUniverse_Ep04.html` | 궤도요소의 기준 epoch와 업데이트 시점 표시 |

### 전자기와 양자

| 파일 | 개선 내용 |
|---|---|
| `dielectric_capacitor_em_hs3_EMQuantum_Ep02.html` | 유전율의 주파수·온도 의존성과 분자 완전 정렬 오해 방지 |
| `matter_wave_em_hs3_EMQuantum_Ep13.html` | 높은 가속전압에서 비상대론적 드브로이 식의 한계 표시 |
| `laser_energy_level_em_hs3_EMQuantum_Ep12.html` | 반전분포·발진 문턱이 매질별 실제값이 아니라 단순 모형이면 명확히 구분 |
| `superconductor_em_hs3_IntegSci1_Matter_Ep08.html` | 임계온도만으로 초전도 상태를 결정하지 않고 임계자기장·임계전류 조건 추가 |

## 공통 기술 사항

- 195개 모두 JavaScript 구문 오류, 중복 ID, 존재하지 않는 고정 DOM 참조가 없었다.
- 모든 파일에 viewport와 반응형 미디어 쿼리가 있었다.
- 대부분 Canvas 애니메이션이므로 실제 360px 화면, 키보드, 연속 클릭, 탭 전환 후 애니메이션 중지 검사가 필요하다.
- 색인 파일은 194개 실험을 표시하므로 파일 추가·삭제 시 목록 수와 링크 존재 여부를 자동 대조하는 검사가 필요하다.

## 우선 수정 순서

1. 완충 용액 `add * 0`
2. 갈바니 전지의 전자 수·반응지수
3. 화석 연대 교집합
4. 상평형도 임의 경계
5. 행성 위성 수와 기준일
6. 기체행성 표면 온도 표현
7. 허블 법칙 적용 거리
8. 개선 필요 34개의 조건·근사·출처 표기

## 다음 검증 범위

- `univGenBio` 12개
- `univMechanics` 14개
- `univEM` 12개
- `fesicsMathLabs` 202개
- `zerolabMathHigh` 68개

이 보고서는 503개 전체 최종본이 아니라, 첫 번째 상세 묶음인 `fesicsLabs` 195개에 대한 결과다.
