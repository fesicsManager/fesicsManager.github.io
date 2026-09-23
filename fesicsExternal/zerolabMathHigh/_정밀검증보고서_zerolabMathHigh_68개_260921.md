# zerolabMathHigh 실험 HTML 68개 정밀 검증 보고서

- 검증일: 2026-09-21
- 대상 폴더: `G:\내 드라이브\Misodle Software\fesicsExternal\zerolabMathHigh`
- 대상: HTML 68개 전부

## 결론

- **즉시 실행을 막는 A급 오류: 0개**
- **수정 권장 B급: 1개**
- **표현 보완 C급: 2개**
- HTML/JavaScript 구문 오류, 중복 ID, 존재하지 않는 요소 참조, 잘못 연결된 label, 외부 의존 파일, TODO/미구현 표시는 발견되지 않았습니다.

## 중점 수정 권장

| 등급 | 파일 | 위치/내용 | 권장 수정 |
|---|---|---|---|
| B | `hs_stat_61_combination_repetition_ProbStat_RepComb_Ep01.html` | 생활 속 예시의 “주사위 여러 개의 눈 조합(순서 무시)”는 보통 서로 구별되는 주사위의 표본공간과 충돌해 학생이 중복조합으로 오해할 수 있음 | “같은 종류의 사탕을 맛별로 r개 고르기” 등 순서를 실제로 무시하는 예시로 교체 |
| C | `hs_calc_56_riemann_sum_Calculus1_Integral_Ep03.html` | “왼쪽 끝 높이(하합), 오른쪽 끝 높이(상합)”은 이 실험의 `y=x², [0,1]`에서는 맞지만 일반 명제로 읽힐 수 있음 | “이 실험처럼 증가하는 함수에서는”이라는 조건 추가 |
| C | `hs_alg_43_geometric_seq_Algebra_Seq_Ep05.html` | 생활 예시 `복리 원리합계(a(1+i)ⁿ⁻¹)`는 a를 최초 원금으로 보는 일반 금융 문맥에서는 기간 수와 지수가 어긋나 보일 수 있음 | `n번째 시점의 항 aₙ=a₁(1+i)ⁿ⁻¹` 또는 `n기간 후 원리합계 A=P(1+i)ⁿ`으로 기준 구분 |

## 검증 범위와 방법

1. 68개 원본 HTML을 각각 내려받아 파일 수·파일명·크기를 확인했습니다.
2. 모든 `<script>`를 파일별로 분리하여 JavaScript 구문 검사를 수행했습니다.
3. DOM의 모든 `id`, `label[for]`, `getElementById`/`$()` 참조를 대조했습니다.
4. 각 파일의 수학 원리, 예시, 공식, 오개념 안내를 주제별로 검토했습니다.
5. 캔버스·입력 슬라이더·라디오·기록·분석 함수의 존재와 연결 구조를 확인했습니다.
6. 외부 URL 의존, 미구현/TODO, 중복 ID를 검사했습니다.

> 참고: 현재 검증 환경에 Chromium 실행 파일이 없어 68개를 실제 브라우저에서 클릭·드래그하는 렌더링 검사는 수행하지 못했습니다. 따라서 “모바일에서 특정 폭에서 겹침”, “애니메이션 도중 클릭”, “캔버스 시각 배치” 같은 실행 전용 항목은 별도 실기 QA가 필요합니다. 다만 구문·DOM 연결·계산 설명은 전 파일을 검사했습니다.

## 파일별 결과


### 공통수학Ⅰ

| 번호 | 파일 | 구조/구문 | 수학 내용 | 비고 |
|---:|---|---|---|---|
| 1 | `hs_c1_01_poly_division_CommonMath1_Poly_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 2 | `hs_c1_02_remainder_theorem_CommonMath1_Poly_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 3 | `hs_c1_03_identity_test_CommonMath1_Poly_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 4 | `hs_c1_04_cube_expansion_CommonMath1_Poly_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 5 | `hs_c1_05_discriminant_CommonMath1_Complex_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 6 | `hs_c1_06_complex_rotation_CommonMath1_Complex_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 7 | `hs_c1_07_conjugate_roots_CommonMath1_Complex_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |
| 8 | `hs_c1_08_roots_coefficients_CommonMath1_Complex_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 9 | `hs_c1_09_quadratic_max_min_CommonMath1_Quad_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 10 | `hs_c1_10_line_parabola_CommonMath1_Quad_Ep01.html` | 통과 | 검토 완료 | 이상 없음 |
| 11 | `hs_c1_11_quadratic_inequality_CommonMath1_Quad_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |
| 12 | `hs_c1_12_cubic_root_count_CommonMath1_Quad_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 13 | `hs_c1_13_perm_vs_comb_CommonMath1_PermComb_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 14 | `hs_c1_14_pascal_symmetry_CommonMath1_PermComb_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 15 | `hs_c1_15_lattice_paths_ProbStat_Perm_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 16 | `hs_c1_16_matrix_dimensions_CommonMath1_Matrix_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 17 | `hs_c1_17_matrix_noncommutative_CommonMath1_Matrix_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 18 | `hs_c1_18_matrix_square_CommonMath1_Matrix_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |

### 공통수학Ⅱ

| 번호 | 파일 | 구조/구문 | 수학 내용 | 비고 |
|---:|---|---|---|---|
| 1 | `hs_c2_19_internal_division_CommonMath2_Shapes_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 2 | `hs_c2_20_perpendicular_slopes_CommonMath2_Shapes_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 3 | `hs_c2_21_point_line_distance_CommonMath2_Shapes_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 4 | `hs_c2_22_circle_line_CommonMath2_Shapes_Ep08.html` | 통과 | 검토 완료 | 이상 없음 |
| 5 | `hs_c2_23_union_count_CommonMath2_SetLogic_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 6 | `hs_c2_24_converse_contrapositive_CommonMath2_SetLogic_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 7 | `hs_c2_25_necessary_sufficient_CommonMath2_SetLogic_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |
| 8 | `hs_c2_26_composite_order_CommonMath2_Func_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 9 | `hs_c2_27_inverse_symmetry_CommonMath2_Func_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 10 | `hs_c2_28_rational_asymptote_CommonMath2_Func_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |

### 대수

| 번호 | 파일 | 구조/구문 | 수학 내용 | 비고 |
|---:|---|---|---|---|
| 1 | `hs_alg_29_nth_root_count_Algebra_ExpLog_Ep01.html` | 통과 | 검토 완료 | 이상 없음 |
| 2 | `hs_alg_30_exponent_laws_Algebra_ExpLog_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 3 | `hs_alg_31_log_definition_Algebra_ExpLog_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 4 | `hs_alg_32_log_laws_Algebra_ExpLog_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 5 | `hs_alg_33_exp_log_inverse_Algebra_ExpLogFunc_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 6 | `hs_alg_34_exp_translation_Algebra_ExpLogFunc_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 7 | `hs_alg_35_exp_inequality_Algebra_ExpLogFunc_Ep08.html` | 통과 | 검토 완료 | 이상 없음 |
| 8 | `hs_alg_36_radian_arc_Algebra_Trig_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 9 | `hs_alg_37_unit_circle_signs_Algebra_Trig_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 10 | `hs_alg_38_sine_wave_Algebra_Trig_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 11 | `hs_alg_39_sine_law_Algebra_TrigApp_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 12 | `hs_alg_40_cosine_law_Algebra_TrigApp_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 13 | `hs_alg_41_triangle_area_Algebra_TrigApp_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 14 | `hs_alg_42_arithmetic_seq_Algebra_Seq_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 15 | `hs_alg_43_geometric_seq_Algebra_Seq_Ep05.html` | 통과 | 표현 보완 | C — 생활 예시의 복리 지수 기준을 명확히 권장 |
| 16 | `hs_alg_44_means_Algebra_Seq_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 17 | `hs_alg_45_sum_first_n_Algebra_Seq_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 18 | `hs_alg_46_geometric_sum_Algebra_Seq_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |
| 19 | `hs_alg_47_sigma_squares_Algebra_Series_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 20 | `hs_alg_48_induction_domino_Algebra_Series_Ep07.html` | 통과 | 검토 완료 | 이상 없음 |

### 미적분Ⅰ

| 번호 | 파일 | 구조/구문 | 수학 내용 | 비고 |
|---:|---|---|---|---|
| 1 | `hs_calc_49_one_sided_limit_Calculus1_Limit_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 2 | `hs_calc_50_indeterminate_Calculus1_Limit_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 3 | `hs_calc_51_continuity_Calculus1_Continuity_Ep01.html` | 통과 | 검토 완료 | 이상 없음 |
| 4 | `hs_calc_52_intermediate_value_Calculus1_Continuity_Ep06.html` | 통과 | 검토 완료 | 이상 없음 |
| 5 | `hs_calc_53_secant_to_tangent_Calculus1_Deriv_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 6 | `hs_calc_54_product_rule_Calculus1_Deriv_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 7 | `hs_calc_55_increase_extremum_Calculus1_DerivApp_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 8 | `hs_calc_56_riemann_sum_Calculus1_Integral_Ep03.html` | 통과 | 표현 보완 | C — 좌합/우합의 하합·상합 설명에 증가함수 조건 명시 권장 |
| 9 | `hs_calc_57_ftc_Calculus1_Integral_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 10 | `hs_calc_58_signed_area_Calculus1_IntegralApp_Ep01.html` | 통과 | 검토 완료 | 이상 없음 |

### 확률과 통계

| 번호 | 파일 | 구조/구문 | 수학 내용 | 비고 |
|---:|---|---|---|---|
| 1 | `hs_stat_59_circular_permutation_ProbStat_Perm_Ep01.html` | 통과 | 검토 완료 | 이상 없음 |
| 2 | `hs_stat_60_same_object_permutation_ProbStat_Perm_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 3 | `hs_stat_61_combination_repetition_ProbStat_RepComb_Ep01.html` | 통과 | 수정 권장 | B — “주사위 여러 개의 눈 조합(순서 무시)” 예시는 오해 가능, 교체 권장 |
| 4 | `hs_stat_62_law_large_numbers_ProbStat_Prob_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 5 | `hs_stat_63_addition_complement_ProbStat_Prob_Ep04.html` | 통과 | 검토 완료 | 이상 없음 |
| 6 | `hs_stat_64_conditional_probability_ProbStat_CondProb_Ep02.html` | 통과 | 검토 완료 | 이상 없음 |
| 7 | `hs_stat_65_independent_exclusive_ProbStat_Prob_Ep05.html` | 통과 | 검토 완료 | 이상 없음 |
| 8 | `hs_stat_66_expected_value_ProbStat_Dist_Ep03.html` | 통과 | 검토 완료 | 이상 없음 |
| 9 | `hs_stat_67_binomial_normal_ProbStat_Dist_Ep06-07.html` | 통과 | 검토 완료 | 이상 없음 |
| 10 | `hs_stat_68_sample_mean_ci_ProbStat_Estim_Ep02-04.html` | 통과 | 검토 완료 | 이상 없음 |

## 배포 전 실기 QA 체크리스트

- 데스크톱(1280×720 이상)과 모바일(360×800)에서 가로 스크롤·텍스트 겹침 확인
- 각 슬라이더 최소/최대값에서 `NaN`, 캔버스 잘림, 축 범위 이탈 확인
- 실행/기록 버튼 연속 클릭 및 애니메이션 중 재클릭 방지 확인
- 기록 4개 이상 생성 후 데이터 검증 탭의 표·결론 갱신 확인
- 표 비우기 후 카운트와 분석 패널 초기화 확인
- 수학 원리 열기/뒤로 가기 및 키보드 포커스 확인

## 판정 기준

- **A급:** 실행 불가, 계산/정답 오류, 핵심 개념 오류
- **B급:** 학습 오개념을 만들 가능성이 높은 예시·설명 오류
- **C급:** 조건·기준을 더 명확히 하면 좋은 표현 또는 UX 보완
