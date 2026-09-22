# fesicsExternal 전수 내용 재검증 보고서 — 배치 3 (중3·고1)

- 검토일: 2026-09-20
- 대상: `3_mid3_high1_87html.zip`
- 범위: 중3 기본·심화 51개, 고1 통합과학 36개, 합계 87개
- 버전 확인: 동봉 `_MANIFEST_SHA256.tsv`의 SHA-256과 87개 전부 일치
- 고1 중복: 번호형 18개와 `integ1_*`/`integ2_*` 18개는 18쌍 모두 바이트 단위 동일
- 판정 합계: **오류 1 / 개선 3 / 양호 83**

## 검증 방법과 한계

각 HTML의 화면 설명, 계산 함수, 슬라이더 범위, 선택지·정답 분기, 버튼·탭·리셋 상태 전이, 표시 단위, 안전 문구를 파일별로 읽고 2026-09-12 지적 사항과 대조했다. 슬라이더는 코드상 최소·중간·최대값, 선택지는 전 분기, 퀴즈는 정답·오답 양쪽, 기록·리셋은 초기화 대상을 추적했다. 고1 동일본은 원본과 복제본의 SHA-256 동일성을 확인한 뒤 같은 코드 경로 판정을 각각 기록했다.

실제 Chromium 실행도 시도했으나 실행 브라우저 바이너리가 환경에 없어 **실제 화면 클릭·애니메이션 프레임 검사는 수행하지 못했다.** 따라서 아래 조작 결과 판정은 정적 코드 경로 검증이다. 2026-09-19 자동검사에서 JS 구문, 중복 ID, 고정 DOM 참조, viewport·media 항목은 전 파일 통과한 상태다.

## 우선 수정 필요 항목

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `milddle3ChemAdv/08_coldpack_limit_lab.html` | **오류** | 215·253·256행은 `도달 온도=max(어는점, 계산 온도)`로 두고 얼기 시작하면 그 어는점에서 멈춘다고 설명한다. 실제 용액은 얼음이 석출되면서 남은 용액 농도가 변해 액상선/어는점도 달라질 수 있어 한 값에 계속 고정되는 일반 법칙이 아니다. 219행은 실제 냉각팩이 “−10℃ 근처가 보통”, 315행은 “보통 0~10℃”라고 해 같은 문서에서 상충한다. | ‘고정된 어는점에서 멈춤’을 교육용 1단계 근사로 명시하거나 농도 변화 모형을 넣는다. 실제 제품 온도 문장은 출처·제품 종류·측정 조건을 붙여 하나로 통일한다. |
| `milddle3Geo/01_atmosphere_layers.html` | 개선 | 본문은 ISA와 85 km 이상 외삽을 정확히 한정했으나, 676행 실행 안내가 여전히 붉은 곡선을 “실제 기온 분포”라고 부른다. | “표준대기 기반 교육용 기온 곡선”으로 변경한다. |
| `milddle3BioAdv/05_nerve_hormone_speed_lab.html` | 개선 | 212행은 거리를 줄여도 호르몬 도달이 빨라지지 않는다고 단정하지만, 221행은 심장과의 거리·혈류·수용체 반응에 따라 달라진다고 올바르게 설명한다. 내부 표현이 충돌한다. | “이 단순 모형에서는 60초로 고정한다”로 한정하고 현실 설명과 분리한다. |
| `milddle3Chem/10_reaction_rules_lab.html` | 개선 | 최종 설명(343행)은 질량비만으로 철을 확정할 수 없다고 수정됐으나, 517행 내부 결론에는 `A는 철`이라는 단정이 남아 있다. 현재는 주석이라 화면에는 직접 노출되지 않지만 유지보수 시 재사용 위험이 있다. | 주석도 “철일 가능성이 큼, 추가 성질 확인 필요”로 통일한다. |

## 중3 생물 13개

| 파일 | 판정 | 검증 결과 |
|---|---|---|
| `milddle3Bio/01_sensory_organs_lab.html` | 양호 | Moon–Spencer 식을 대표 모형으로 한정하고 개인차·적응·조건을 보완함. 수식·단위·판정 분기 일치. |
| `milddle3Bio/02_hearing_smell_taste_lab.html` | 양호 | 가청 주파수·미각 역치의 개인차와 검사 조건, 산 용액 직접 시험 금지 안내 확인. |
| `milddle3Bio/03_neuron_pathway_lab.html` | 양호 | 전도 속도값을 대표값으로 한정하고 말이집 외 축삭 지름·온도·신경 종류 영향 명시. |
| `milddle3Bio/04_reflex_conscious_response_lab.html` | 양호 | 반응 시간의 개인차와 회피반사의 뇌 전달을 구분함. 경로·퀴즈 판정 일치. |
| `milddle3Bio/05_hormones_lab.html` | 양호 | 일반 식사와 75 g 경구당부하검사를 구분하고 140/200 mg/dL 경계, 재검사·다른 진단 기준 필요성을 명시함. |
| `milddle3Bio/06_mitosis_lab.html` | 양호 | 2ⁿ 계산을 한 세포 계통의 동기적 분열 가정으로 한정함. 10회→1,024개 계산 일치. |
| `milddle3Bio/07_meiosis_lab.html` | 양호 | 이배체 체세포·생식세포 염색체 수와 감수 1·2분열 설명·정답 일치. |
| `milddle3Bio/08_embryonic_development_lab.html` | 양호 | 일자별 세포 수·크기를 대표 범위로 한정하고 개인·배양 조건 차이 명시. |
| `milddle3Bio/09_mendel_law_lab.html` | 양호 | Yy×Yy 확률, 무작위 표본, 큰 표본에서 3:1 접근 설명·판정 일치. |
| `milddle3Bio/10_human_heredity_summary_lab.html` | 양호 | 단일유전자 모형 한계, ABO 복대립유전 계산과 정답 분기 적절. |
| `milddle3BioAdv/05_nerve_hormone_speed_lab.html` | 개선 | 60초 고정은 교육용 대표값이라고 밝혔으나 본문 한 문장이 현실에서도 거리 무관으로 읽힘. 우선 수정표 참조. |
| `milddle3BioAdv/06_division_cycle_lab.html` | 양호 | 세포주·배양 조건별 주기 차이와 성장곡선 단계 한계를 표시함. 계산·단위 일치. |
| `milddle3BioAdv/07_chromosome_number_lab.html` | 양호 | ‘이배체·정상 감수분열’ 조건을 명시해 생식세포가 절반이라는 일반화 오류를 해소함. |

## 중3 화학 13개

| 파일 | 판정 | 검증 결과 |
|---|---|---|
| `milddle3Chem/01_mass_conservation_lab.html` | 양호 | 밀폐계 조건, 반응 전후 질량 합, 단위와 정답 일치. |
| `milddle3Chem/02_open_container_lab.html` | 양호 | 식초 충분·완전 반응 조건과 CO₂ 손실 단순 모형을 명시함. |
| `milddle3Chem/03_iron_rust_lab.html` | 양호 | 시간당 증가를 교육용 선형 모형으로 한정하고 수분·산소·표면적·속도 저하를 안내함. |
| `milddle3Chem/04_definite_proportions_lab.html` | 양호 | CuO의 구리:산소 약 4:1 질량비, 생성물 계산·단위 일치. |
| `milddle3Chem/05_limiting_reactant_lab.html` | 양호 | 산소 고정 조건에서 반응 구리·남는 구리 계산과 판정 일치. |
| `milddle3Chem/06_water_electrolysis_lab.html` | 양호 | 2:1 부피비에 같은 온도·압력 및 전해질·전극 조건을 보완함. |
| `milddle3Chem/07_exothermic_lab.html` | 양호 | 철가루–온도 관계를 교육용 모형으로 한정하고 열용량·산소·열손실 한계를 명시함. |
| `milddle3Chem/08_endothermic_lab.html` | 양호 | 용액 열용량·용해도·주변 열교환을 한계로 표시함. 부호·℃ 단위 일치. |
| `milddle3Chem/09_combustion_energy_lab.html` | 양호 | 완전연소·고정 발열량 조건에서 연료량과 열량 계산 일치. |
| `milddle3Chem/10_reaction_rules_lab.html` | 개선 | 화면 최종 설명은 철 ‘가능성’으로 수정됐으나 내부 주석에 확정 표현 잔존. |
| `milddle3ChemAdv/02_mass_loss_calc_lab.html` | 양호 | 식초 과량·반응 완결 조건을 명시하고 CO₂ 질량 손실 계산 일치. |
| `milddle3ChemAdv/07_heatpack_temp_lab.html` | 양호 | 선형 ΔT를 교육용 대표 모형으로 한정하고 계 열용량·산소·열손실·속도 한계를 명시함. |
| `milddle3ChemAdv/08_coldpack_limit_lab.html` | 오류 | 어는점 고정 처리의 과학적 일반화와 실제 제품 온도 문장 상충. 우선 수정표 참조. |

## 중3 지구과학 14개

| 파일 | 판정 | 검증 결과 |
|---|---|---|
| `milddle3Geo/01_atmosphere_layers.html` | 개선 | ISA 범위·열권 외삽 한계는 보완됐으나 실행 안내의 “실제 기온 분포” 표현 잔존. |
| `milddle3Geo/02_pressure_wind.html` | 양호 | 풍속식을 교육용 모형으로 한정하고 전향력·마찰·밀도 영향을 명시함. |
| `milddle3Geo/03_clouds_precipitation.html` | 양호 | 온도 수직분포·온층 깊이·따뜻한 비 과정의 예외를 보완함. |
| `milddle3Geo/04_air_mass_front.html` | 양호 | 전선별 전형을 계절·수증기·안정도·이동속도에 따른 대표 경향으로 한정함. |
| `milddle3Geo/05_weather_forecast.html` | 양호 | `90−0.07d+25`를 실제 예보식이 아닌 교육용 가상 모형으로 반복 명시함. |
| `milddle3Geo/06_star_magnitude.html` | 양호 | 거리 지수, 겉보기·절대등급 관계와 순위 해석 일치. |
| `milddle3Geo/07_star_color.html` | 양호 | 태양광은 본질적으로 흰색에 가깝고 별 색은 전체 스펙트럼·시각 반응으로 정해짐을 보완함. |
| `milddle3Geo/08_galaxy_scale.html` | 양호 | 태양계·은하 축척과 태양 위치 계산·단위 일치. |
| `milddle3Geo/09_universe_scale.html` | 양호 | 풍선 표면 모형의 차원·중심 해석 한계와 묶인 계의 차이를 명시함. |
| `milddle3Geo/10_space_exploration_reason.html` | 양호 | 인공위성 정의, 궤도 이동 한계, 파생기술의 ‘개량’ 구분을 수정함. 거리÷17 km/s 계산도 일치. |
| `milddle3GeoAdv/02_altitude_pressure_lab.html` | 양호 | 기압 반감·끓는점 관계를 제한 구간 근사로 명시함. |
| `milddle3GeoAdv/05_isobar_wind_lab.html` | 양호 | 반비례식을 교육용 모형으로 한정하고 전향력·마찰·곡률·밀도 영향을 보완함. |
| `milddle3GeoAdv/06_apparent_absolute_lab.html` | 양호 | 거리 지수, 등급 부호, 밝기 순위와 정답 일치. |
| `milddle3GeoAdv/09_hubble_age_lab.html` | 양호 | 가까운 은하 고유운동, H₀ 불확실성, 우주 팽창사 때문에 `1/H₀`가 근사임을 명시함. |

## 중3 물리 11개

| 파일 | 판정 | 검증 결과 |
|---|---|---|
| `milddle3Phy/01_uniform_motion_lab.html` | 양호 | 등속 2.0 m/s에서 거리–시간 기울기·단위·정답 일치. |
| `milddle3Phy/02_speed_conversion_lab.html` | 양호 | km/h↔m/s 환산 3.6, 경계값과 판정 일치. |
| `milddle3Phy/03_graph_area_lab.html` | 양호 | 구간별 속력×시간과 그래프 넓이의 이동 거리 계산 일치. |
| `milddle3Phy/04_air_resistance_lab.html` | 양호 | 질량·면적·항력계수를 대표 모형값으로 한정하고 자세·형상·공기 조건 한계 명시. |
| `milddle3Phy/05_gravity_acceleration_lab.html` | 양호 | 무저항 조건의 `v=gt`, `h=½gt²`, g와 단위 일치. |
| `milddle3Phy/06_freefall_ride_lab.html` | 양호 | `v=√(2gh)` 계산, 높이 경계값·단위·정답 일치. |
| `milddle3Phy/07_pendulum_energy_lab.html` | 양호 | 비선형 진자와 에너지 보존 계산이 일관되고 길이·각도 조건 표시. |
| `milddle3Phy/08_energy_conservation_lab.html` | 양호 | 마찰 없는 1 kg 수레의 위치·운동·역학적 에너지 합 일치. |
| `milddle3Phy/09_friction_loss_lab.html` | 양호 | 마찰 일, 열 전환, 남은 운동에너지의 부호·단위 일치. |
| `milddle3Phy/10_projectile_motion_lab.html` | 양호 | 무저항 수평투사에서 수평·수직 독립, 낙하시간 계산 일치. |
| `milddle3PhyAdv/06_freefall_speed_design_lab.html` | 양호 | 자유낙하 역산식을 실제 설계 전체가 아닌 1차 물리 모형으로 한정함. |

## 고1 통합과학 36개

아래 번호형 18개와 별칭형 18개는 쌍별 SHA-256이 같다. 모든 쌍에서 수식·단위·정답·조작 분기가 동일하며, 이전 개선 요구(모형 범위·가정 지속 표시)가 현재 화면 설명에 반영됐다.

| 파일 | 판정 | 핵심 확인 |
|---|---|---|
| `high1Integ/01_gps_clock_error_lab_IntegSci1_Basics_Ep01_Adv01.html` | 양호 | 상대론적 시계 오차의 부호·누적·단위와 모형 조건 일치. |
| `high1Integ/02_big_bang_helium_lab_IntegSci1_Matter_Ep01_Adv01.html` | 양호 | 수소·헬륨 비율을 단순 핵합성 모형으로 한정. |
| `high1Integ/03_line_spectrum_lab_IntegSci1_Matter_Ep01-02_Adv01.html` | 양호 | 선스펙트럼 원소 판별과 파장 단위·정답 일치. |
| `high1Integ/04_conductivity_bonding_lab_IntegSci1_Matter_Ep05_Adv03.html` | 양호 | 고체/용융/수용액 전도성과 결합 모형 분기 일치. |
| `high1Integ/05_free_fall_projectile_lab_IntegSci1_Systems_Ep01_Adv03.html` | 양호 | 무저항 자유낙하·투사 운동의 g, 시간, 거리 관계 일치. |
| `high1Integ/06_impulse_egg_drop_lab_IntegSci1_Systems_Ep02_Adv04.html` | 양호 | 충격량–평균힘 관계와 완충시간 모형 조건 표시. |
| `high1Integ/07_momentum_ice_push_lab_IntegSci1_Systems_Ep02_Adv04.html` | 양호 | 운동량 보존, 방향 부호와 질량·속도 단위 일치. |
| `high1Integ/08_seafloor_spreading_lab_IntegSci1_Systems_Ep04_Adv05.html` | 양호 | 거리–연령–확장속도 관계를 일정 속도 모형으로 한정. |
| `high1Integ/09_dna_mutation_codon_lab_IntegSci1_Systems_Ep05_Adv06.html` | 양호 | 코돈 변화·아미노산 판정과 침묵/과오/종결 분기 일치. |
| `high1Integ/10_natural_selection_antibiotic_lab_IntegSci2_Change_Ep03_Adv02.html` | 양호 | 내성 빈도 변화가 유도 변이가 아닌 선택 모형임을 명시. |
| `high1Integ/11_neutralization_heat_lab_IntegSci2_Change_Ep07_Adv04.html` | 양호 | 산·염기 몰수, 제한 반응물, 중화열·온도 변화 단위 일치. |
| `high1Integ/12_exo_endo_pack_lab_IntegSci2_Change_Ep08_Adv04.html` | 양호 | 발열/흡열 방향과 물·용질 양에 따른 교육용 열수지 분기 일치. |
| `high1Integ/13_greenhouse_blanket_lab_IntegSci2_EnvEnergy_Ep03_Adv06.html` | 양호 | 온실효과 수치를 단순 에너지수지 모형으로 한정. |
| `high1Integ/14_fox_island_lab_IntegSci2_EnvEnergy_Ep02_Adv05.html` | 양호 | 포식–피식 개체군 변화와 수용력 모형·판정 일치. |
| `high1Integ/15_electromagnetic_induction_lab_IntegSci2_EnvEnergy_Ep06_Adv08.html` | 양호 | 자속 변화율·감은 수·유도전압 방향/크기 관계 일치. |
| `high1Integ/16_energy_efficiency_relay_lab_IntegSci2_EnvEnergy_Ep08_Adv08.html` | 양호 | 효율 곱셈, 입력·유용·손실 에너지 단위 일치. |
| `high1Integ/17_epidemic_spread_lab_IntegSci2_Future_Ep01.html` | 양호 | 감염 확산을 교육용 확률 모형으로 한정하고 실제 예측 한계 명시. |
| `high1Integ/18_correlation_causation_lab_IntegSci2_Future_Ep02.html` | 양호 | 상관과 인과, 교란변수 판단·정답 분기 일치. |
| `high1Integ/integ1_gps_clock_error_IntegSci1_Basics_Ep01_Adv01.html` | 양호 | 01번과 동일본. |
| `high1Integ/integ1_big_bang_helium_IntegSci1_Matter_Ep01_Adv01.html` | 양호 | 02번과 동일본. |
| `high1Integ/integ1_line_spectrum_IntegSci1_Matter_Ep01-02_Adv01.html` | 양호 | 03번과 동일본. |
| `high1Integ/integ1_conductivity_bonding_IntegSci1_Matter_Ep05_Adv03.html` | 양호 | 04번과 동일본. |
| `high1Integ/integ1_free_fall_projectile_IntegSci1_Systems_Ep01_Adv03.html` | 양호 | 05번과 동일본. |
| `high1Integ/integ1_impulse_egg_drop_IntegSci1_Systems_Ep02_Adv04.html` | 양호 | 06번과 동일본. |
| `high1Integ/integ1_momentum_ice_push_IntegSci1_Systems_Ep02_Adv04.html` | 양호 | 07번과 동일본. |
| `high1Integ/integ1_seafloor_spreading_IntegSci1_Systems_Ep04_Adv05.html` | 양호 | 08번과 동일본. |
| `high1Integ/integ1_dna_mutation_codon_IntegSci1_Systems_Ep05_Adv06.html` | 양호 | 09번과 동일본. |
| `high1Integ/integ2_natural_selection_antibiotic_IntegSci2_Change_Ep03_Adv02.html` | 양호 | 10번과 동일본. |
| `high1Integ/integ2_neutralization_heat_IntegSci2_Change_Ep07_Adv04.html` | 양호 | 11번과 동일본. |
| `high1Integ/integ2_exo_endo_pack_IntegSci2_Change_Ep08_Adv04.html` | 양호 | 12번과 동일본. |
| `high1Integ/integ2_greenhouse_blanket_IntegSci2_EnvEnergy_Ep03_Adv06.html` | 양호 | 13번과 동일본. |
| `high1Integ/integ2_fox_island_IntegSci2_EnvEnergy_Ep02_Adv05.html` | 양호 | 14번과 동일본. |
| `high1Integ/integ2_electromagnetic_induction_IntegSci2_EnvEnergy_Ep06_Adv08.html` | 양호 | 15번과 동일본. |
| `high1Integ/integ2_energy_efficiency_relay_IntegSci2_EnvEnergy_Ep08_Adv08.html` | 양호 | 16번과 동일본. |
| `high1Integ/integ2_epidemic_spread_IntegSci2_Future_Ep01.html` | 양호 | 17번과 동일본. |
| `high1Integ/integ2_correlation_causation_IntegSci2_Future_Ep02.html` | 양호 | 18번과 동일본. |

## 안전성·조작 결과 종합

- 위험 가능성이 있는 산 용액 맛보기, 냉각팩 피부 접촉, 화학물질·전기 관련 활동은 직접 실행 지시가 아니라 시뮬레이션이며 관련 주의 문구를 확인했다.
- 냉각팩에는 동상 위험과 수건 사용 안내가 있다. 감각 실험에는 산 용액 직접 시험 금지가 있다.
- 코드상 슬라이더 최소·중간·최대, 선택 버튼 전 분기, 퀴즈 정답·오답, 기록 추가·리셋 경로에서 단위 누락이나 정답 역전은 발견하지 못했다.
- 고1 동일본은 한쪽 수정 시 다른 파일이 자동으로 바뀌지 않으므로, 향후 수정 때 18쌍을 함께 반영하거나 중복 파일을 단일 소스로 생성하는 편이 안전하다.

## 이전 지적 사항 수정 확인

- 2026-09-12의 중3 오류·개선 사항 중 혈당 진단, 냉각팩 0℃ 고정, 대기·바람·강수·별 색, 우주탐사 정의, 철 손난로, 호르몬 속도 등은 대부분 설명·가정 문구가 반영됐다.
- 다만 냉각팩은 0℃ 고정 오류를 없애는 과정에서 ‘한 번 계산한 용액 어는점에 계속 고정’하는 새 과도 단순화와 온도 범위 상충이 남았다.
- 대기층, 신경–호르몬, 반응 규칙은 핵심 결론은 수정됐지만 일부 실행 문구·주석이 새 설명과 완전히 통일되지 않았다.
- 고1의 이전 개선 9종과 동일 복제본 9종은 모형 범위·조건 표시가 반영된 것을 확인했다.

## 완료 선언

**검토 완료 파일 수 87 / 전체 87.** 87개 모두 파일별 내용·수식·정답·단위·안전 문구·정적 조작 분기를 확인했다. 실제 브라우저 상호작용 검사는 환경상 미수행이며, 수정 우선순위는 냉각팩 오류 1건 → 표현 불일치 개선 3건 순이다.
