# fesicsExternal 상세 검증 2 — 대학 38개

- 대상: `univGenBio` 12개, `univMechanics` 14개, `univEM` 12개
- 검증: JavaScript·DOM·접근성·반응형 구조, 수식·설명·계산 모형 대조
- 원본 변경 없음

## 요약

| 폴더 | 오류 | 개선 필요 | 양호 | 합계 |
|---|---:|---:|---:|---:|
| univGenBio | 2 | 7 | 3 | 12 |
| univMechanics | 2 | 5 | 7 | 14 |
| univEM | 1 | 5 | 6 | 12 |
| **합계** | **5** | **17** | **16** | **38** |

## 오류 5개

1. `univGenBio/genbio_lab11_antibiotic_GenBio2_Wk02.html`
   - MRSA가 β-락탐 “전부”에 내성이라고 단정한다. 항-MRSA 세팔로스포린 예외가 있으므로 “대부분의 β-락탐”으로 수정하고 CLSI/EUCAST 판본을 표시해야 한다.
2. `univGenBio/genbio_lab06_mendel_chisquare_GenBio1_Wk12.html`
   - 유의하지 않은 결과를 “가설 채택”이라고 표현한다. “귀무가설을 기각하지 못함”으로 수정해야 한다.
3. `univMechanics/cm_sim14_spinning_top_ClassMech_Wk09.html`
   - 유효 퍼텐셜이 θ 양 끝에서 언제나 무한대라 팽이가 절대 완전히 서거나 눕지 못한다고 단정한다. 특정 보존 각운동량 관계에서는 특이성이 상쇄될 수 있으므로 일반적인 경우로 한정해야 한다.
4. `univMechanics/cm_sim10_rutherford_ClassMech_Wk07.html`
   - 전자 차폐 때문에 충분히 멀리서 힘이 “실제로 0”이라고 한다. 정확히 0이 아니라 빠르게 감소해 무시 가능해지는 것으로 수정해야 한다.
5. `univEM/univ_em_10_biot_savart_EM_Ep09.html`
   - `∮B·dl=μ₀I_enc`가 항상 성립한다고 먼저 단정한다. 시간 변화가 있으면 변위전류 항이 필요하므로 첫 문장부터 정상전류 조건으로 제한해야 한다.

## 개선 필요 17개

### 일반생물 7개

- `genbio_lab01_enzyme_kinetics_GenBio1_Wk06.html`: Km을 곧바로 친화도 척도로 단정하지 말고 속도상수에도 의존함을 표시.
- `genbio_lab02_osmosis_GenBio1_Wk05.html`: 감자 조직의 압력퍼텐셜 및 조직 손상·용질 침투 조건 보완.
- `genbio_lab03_photosynthesis_GenBio1_Wk08.html`: 고정 Pmax·IK·Q10을 모형값으로 계속 표시.
- `genbio_lab05_population_growth_GenBio2_Wk15.html`: 로지스틱 K가 시간에 따라 달라질 수 있고 지체·사멸기를 설명하지 못하는 한계 표시.
- `genbio_lab08_electrophoresis_GenBio2_Wk03.html`: 이동거리–log(bp) 직선 관계는 젤 농도와 유효 범위 안의 근사임을 표시.
- `genbio_lab09_diffusion_sa_v_GenBio1_Wk04-05.html`: 침투 깊이 √(2Dt)는 특성 길이이며 색 변화 문턱·경계조건에 따라 달라짐을 표시.
- `genbio_lab12_exercise_physiology_GenBio2_Wk11.html`: 최대심박 200−나이와 PFI 고정 등급의 출처·적용 집단·개인차 표시.

### 고전역학 5개

- `cm_sim01_brachistochrone_ClassMech_Wk01.html`: 점질량·무마찰·회전 없는 미끄럼 조건을 결과 근처에 표시.
- `cm_sim04_double_pendulum_ClassMech_Wk04.html`: “절대 정확히 반복되지 않음”은 이상적 무리수 비 조건으로 한정.
- `cm_sim08_symmetry_canonical_ClassMech_Wk05_Wk14.html`: 유한 시간 수치적분의 보존 오차를 “기계 정밀도”로 일반화하지 않도록 적분법·간격 표시.
- `cm_sim19_phase_space_ClassMech_Wk12-13.html`: 자유낙하처럼 비구속 계에서 표시 영역 밖 이동과 면적 산정 조건 보완.
- `cm_sim23_poincare_ClassMech_Wk15.html`: 유한 적분시간·표본 수로 규칙/카오스를 확정하지 않도록 판정 한계 표시.

### 전자기학 5개

- `univ_em_01_vector_field_EM_Ep01.html`: 2차원 면적 기반 회전 설명과 3차원 스토크스 정리의 면 법선 방향을 구분.
- `univ_em_03_gauss_symmetry_EM_Ep03.html`: 계산 가능한 대칭을 “세 가지뿐”이라고 단정하지 말고 교과서의 대표 세 유형으로 표현.
- `univ_em_05_conductor_EM_Ep05.html`: “알짜 전하는 모두 표면”은 정전평형의 균질 도체 조건임을 표시.
- `univ_em_11_magnetization_EM_Ep11.html`: 반자성을 모든 물질에서 온도 무관·동일 기작으로 읽히지 않도록 보완하고 히스테리시스 모형의 임의 매개변수 표시.
- `univ_em_12_emwave_EM_Ep15.html`: 좋은 도체 근사에서의 E–B 위상차·표피깊이 조건과 일반 도체를 구분.

## 기술 검사

- 38개 모두 인라인 JavaScript 구문 통과.
- 중복 ID 및 존재하지 않는 고정 DOM 참조 없음.
- 입력 요소 접근성 이름과 반응형 CSS는 모두 확인됨.
- `univMechanics` 14개는 외부 MathJax CDN에 의존하므로 오프라인 수업에서 수식이 렌더링되지 않을 수 있음.

## 양호 16개

- 일반생물: `genbio_lab04_hardy_weinberg`, `genbio_lab07_respiration`, `genbio_lab10_biodiversity`
- 고전역학: `cm_sim07_spring_pendulum`, `cm_sim09_effective_potential`, `cm_sim11_inertia_ellipsoid`, `cm_sim13_intermediate_axis`, `cm_sim15_normal_modes`, `cm_sim17_dispersion`, `cm_sim22_torus`
- 전자기학: `univ_em_02_delta_function`, `univ_em_04_potential`, `univ_em_06_image_charge`, `univ_em_07_laplace`, `univ_em_08_multipole`, `univ_em_09_dielectric`

## 다음 범위

- `fesicsMathLabs` 202개
- `zerolabMathHigh` 68개
