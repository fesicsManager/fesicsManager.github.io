# fesicsExternal 추가 검증보고서

- 검증일: 2026-09-14
- 대상: Google Drive `Misodle Software/github/fesicsExternal`
- 기준 보고서: `_검증보고서_fesicsExternal_HTML_260912.md` (기존 교과 폴더 50개, HTML 405개)
- 원본 처리: 읽기 전용 검증, 원본 변경 없음

## 1. 추가 범위

| 폴더 | HTML | 비고 |
|---|---:|---|
| `fesicsLabs` | 195 | 색인 1개 + 과학 실험 194개 |
| `univGenBio` | 12 | 대학 일반생물 |
| `univMechanics` | 14 | 대학 고전역학 (`README.md` 제외) |
| `univEM` | 12 | 대학 전자기학 (`README.md` 제외) |
| `fesicsMathLabs` | 202 | 색인 1개 + 수학 실험 201개 |
| `zerolabMathHigh` | 68 | 고등 수학 |
| **합계** | **503** | 기존 405개와 별도 추가 검증 |

현재 누적 검증 HTML은 기존 405개 + 신규 503개 = **908개**다. 루트 `index.html`은 2026-09-14에 수정됐으나 교과 실험 판정 수에는 포함하지 않았다.

## 2. 자동 정적 검사 결과

| 검사 항목 | 결과 |
|---|---:|
| JavaScript 인라인 구문 오류 | 0개 |
| 존재하지 않는 고정 ID 참조 | 0개 |
| 중복 `id` | 0개 |
| viewport 메타 누락 | 0개 |
| 반응형 `@media` 누락 | 0개 |
| 접근성 이름 없는 입력 요소 포함 파일 | 15개 |
| 외부 스크립트 의존 파일 | 14개 |

503개 모두 기본 구조는 안정적이다. 다만 이 결과는 소스 정적 검사이며, 모든 클릭 순서·애니메이션·모바일 렌더링의 정상 동작을 보증하지 않는다.

## 3. 즉시 수정 권장

### A. 수학 내용 오류

1. `zerolabMathHigh/hs_c1_12_cubic_root_count_CommonMath1_Quad_Ep04.html`
   - 현재 설명은 “삼차방정식의 실근은 1개 또는 3개”라고 한 뒤 `(x−1)²(x+2)=0`을 예로 든다.
   - 이 예의 **서로 다른 실근은 1, −2의 2개**다. 중복도를 포함하면 실근 3개이고, 서로 다른 근을 세면 2개다.
   - `중복도를 포함해 세면 복소수 근은 3개`, `서로 다른 실근은 1·2·3개가 가능`으로 기준을 분리해야 한다.

### B. 대학 생물 내용 오류·과도한 일반화

2. `univGenBio/genbio_lab11_antibiotic_GenBio2_Wk02.html`
   - MRSA가 “β-락탐 전부”에 내성이라고 단정한다. 항-MRSA 활성이 있는 일부 세팔로스포린 예외가 있으므로 `대부분의 β-락탐`으로 고치고, 판정 기준은 균종·약제·CLSI/EUCAST 판본에 따라 달라짐을 표시해야 한다.

3. `univGenBio/genbio_lab06_mendel_chisquare_GenBio1_Wk12.html`
   - 카이제곱 결과를 `가설 채택`이라고 표현한다. 유의하지 않은 결과는 귀무가설을 증명한 것이 아니므로 `귀무가설을 기각하지 못함`으로 고쳐야 한다.

4. `univGenBio/genbio_lab01_enzyme_kinetics_GenBio1_Wk06.html`
   - `K_m`을 곧바로 효소–기질 친화도의 척도라고 설명한다. 단순 미카엘리스–멘텐 기작의 특정 조건에서만 해리 특성과 연결되므로 `작을수록 친화도가 높다고 해석하는 경우가 많지만 반응 속도 상수에도 의존`이라는 조건을 붙여야 한다.

5. `univGenBio/genbio_lab12_exercise_physiology_GenBio2_Wk11.html`
   - 최대 심박 `200−나이`와 PFI 고정 구간을 일반 기준처럼 사용한다. 공식·판정표의 출처와 적용 집단을 밝히고, 개인차·복용약·측정 프로토콜에 따른 차이를 안내해야 한다.

### C. 대학 물리 내용 오류·조건 누락

6. `univEM/univ_em_10_biot_savart_EM_Ep09.html`
   - 핵심 설명에서 `∮B·dl = μ₀I_enc`가 “항상” 성립한다고 먼저 단정한 뒤 아래에서 변위전류 항을 추가한다.
   - 시간 변화가 있는 일반식은 `∮B·dl = μ₀(I_enc + ε₀ dΦ_E/dt)`다. 첫 설명부터 `정상 전류 조건`으로 한정해야 한다.

7. `univMechanics/cm_sim14_spinning_top_ClassMech_Wk09.html`
   - 유효 퍼텐셜이 θ의 양 끝에서 항상 무한대이므로 팽이가 절대 완전히 서거나 눕지 못한다고 단정한다.
   - 보존 각운동량의 특수 관계에서는 한쪽 특이성이 상쇄될 수 있다. 초기조건·보존량 조건을 명시하고 `일반적인 경우`로 완화해야 한다.

8. `univMechanics/cm_sim10_rutherford_ClassMech_Wk07.html`
   - 원자의 전자 차폐 때문에 충분히 멀리서 힘이 “실제로 0”이라고 표현한다.
   - 중성 원자의 유효 퍼텐셜은 빠르게 감소하지만 유한 거리에서 정확히 0이라고 단정할 수 없다. `빠르게 작아져 무시할 수 있다`로 고치는 편이 정확하다.

## 4. 접근성 수정 대상 15개

`label`, `aria-label` 또는 동등한 접근성 이름이 없는 입력 요소가 확인됐다.

- `fesicsMathLabs/index.html` — 1개
- `zerolabMathHigh/hs_stat_65_independent_exclusive_ProbStat_Prob_Ep05.html` — 8개
- `zerolabMathHigh/hs_stat_63_addition_complement_ProbStat_Prob_Ep04.html` — 8개
- `zerolabMathHigh/hs_stat_62_law_large_numbers_ProbStat_Prob_Ep02.html` — 3개
- `zerolabMathHigh/hs_calc_56_riemann_sum_Calculus1_Integral.html` — 3개
- `zerolabMathHigh/hs_calc_53_secant_to_tangent_Calculus1_Deriv_Ep02.html` — 3개
- `zerolabMathHigh/hs_calc_50_indeterminate_Calculus1_Limit_Ep05.html` — 4개
- `zerolabMathHigh/hs_calc_49_one_sided_limit_Calculus1_Limit_Ep02.html` — 4개
- `zerolabMathHigh/hs_c2_25_necessary_sufficient_CommonMath2_SetLogic_Ep07.html` — 8개
- `zerolabMathHigh/hs_c2_24_converse_contrapositive_CommonMath2_SetLogic_Ep06.html` — 8개
- `zerolabMathHigh/hs_c1_18_matrix_square_CommonMath1_Matrix_Ep05.html` — 4개
- `zerolabMathHigh/hs_c1_17_matrix_noncommutative_CommonMath1_Matrix_Ep05.html` — 4개
- `zerolabMathHigh/hs_c1_11_quadratic_inequality_CommonMath1_Quad_Ep07.html` — 2개
- `zerolabMathHigh/hs_c1_01_poly_division_CommonMath1_Poly_Ep04.html` — 2개
- `zerolabMathHigh/hs_alg_48_induction_domino_Algebra_Series_Ep07.html` — 4개

## 5. 외부 의존성과 성능

- `univMechanics`의 HTML 14개 모두 `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js`에 의존한다. 학교망 차단이나 오프라인 수업에서는 수식 렌더링이 실패할 수 있으므로 로컬 번들 또는 대체 표시를 준비하는 것이 좋다.
- 503개 중 501개가 `<canvas>`를 사용하고, 493개가 `requestAnimationFrame`을 호출한다. 정지 화면에서도 프레임 루프가 계속되는지 실제 브라우저 성능 검사로 확인해야 한다.
- 모든 파일에 반응형 CSS와 viewport 설정은 있으나, 360px 화면에서 캔버스·표·수식·버튼이 잘리지 않는지는 별도 실브라우저 검사가 필요하다.

## 6. 우선순위

1. 삼차방정식 실근 개수 설명을 먼저 수정한다.
2. MRSA β-락탐, 카이제곱 `가설 채택`, 앙페르 법칙 `항상` 표현을 수정한다.
3. 접근성 누락 15개 파일에 입력 이름을 추가한다.
4. 대학 고전역학 14개의 MathJax 오프라인 대응을 정한다.
5. 실제 브라우저에서 360px, 키보드, 연속 클릭, 애니메이션 종료, 표/캔버스 크기를 확인한다.

## 판정

추가된 503개는 기본 코드 구조와 반응형 뼈대는 전반적으로 양호하다. 즉시 수정할 명확한 내용 문제 8개 항목과 접근성 누락 15개 파일이 있으며, 대학 고전역학의 외부 수식 라이브러리 의존과 대규모 캔버스 애니메이션은 배포 전 실브라우저 확인이 필요하다.
