# 재검증보고서 — fesicsExternal 배치 4 (고2·고3 125 HTML)

- 검토일: 2026-09-20
- 대상: `4_high2_high3_125html.zip`
- 기준: 동봉 `_MANIFEST_SHA256.tsv`의 스냅샷
- Google Drive 업로드: 하지 않음

## 결론

- 검토 완료: **125 / 125 HTML**
- 판정: **오류 1개 / 개선 14개 / 양호 110개**
- 과거 중대 오류 7건: **7건 모두 수정 반영 확인**
- 과거 개선 권고 50건: 모형 한계·조건 문구의 반영을 확인함. 다만 이번 검토에서 별도로 안전 문구 부족과 내부 수치 불일치를 발견함.

## 검증 방법과 범위

1. 각 HTML의 원리 설명, 예시 계산, `compute()` 계산식, 결과 표·판정 문구, 단위와 범위를 파일별로 대조했다.
2. 선택형 입력의 전 조합 또는 입력 수가 큰 경우 기본값+각 축 경계+2축 조합을 실행했다. 총 **13,893개 계산 조합**에서 예상된 `Q=∞` 표기 외 NaN·무한대·예외가 없었다.
3. 버튼·기록·초기화·탭은 공통 엔진의 상태 흐름과 파일별 `compute/draw/record/verify` 연결을 정적으로 추적했다.
4. 이 환경에는 실행 가능한 Chromium 바이너리가 없어 실제 브라우저 클릭·애니메이션·360 px 렌더링은 수행하지 못했다. 따라서 “모든 조작 결과”는 코드 경로 기준 검증이며 실제 렌더링 보증은 아니다.

## 중요 발견

### 오류 1건

- `high3MatterEnergy/01_reaction_enthalpy_lab_MatterEnergy_Ep08.html`: 설명의 중화 엔탈피와 온도 상승 예시가 코드의 상수·열량계 모델과 일치하지 않는다. 설명은 −57.3 kJ/mol 및 약 +6.9 ℃(234행), 코드는 −56.1 kJ/mol(447행)이며 계산에는 용질 질량과 열량계 열용량 15 J/℃도 포함한다. 같은 조건으로 다시 계산해 문구와 코드 중 하나를 통일해야 한다.

### 개선 14건

- 안전 문구 부족 13건: 산·염기, NaOH, 레이저, 전기분해, 수소/산소, SO₂ 발생 실험에서 보안경·환기·점화원 차단·교사 감독·폐액 안내가 빠져 있다.
- 개념 표현 1건: 약산이 강산보다 pH가 높다는 이유만으로 “마실 수 있다”고 연결한 문구는 음용 안전성을 지나치게 단순화한다.

### 과거 중대 오류 7건 수정 확인

| 파일 | 확인 결과 |
|---|---|
| `high2Geo/08_geologic_time_fossil...` | Ma 축에서 `min(start), max(end)`가 교집합임을 설명·예시와 일치시킴 |
| `high2Geo/16_hubble_law...` | `z<0.15`, 최대 570 Mpc로 범위 제한 |
| `high3ChemReaction/03_titration_buffer...` | 강산·물 모두 H⁺/OH⁻ 중화 후 남은 몰수로 pH 계산 |
| `high3ChemReaction/06_galvanic_cell...` | 전자 수 최소공배수와 Q의 화학양론 지수 반영 |
| `high3MatterEnergy/06_phase_diagram...` | 정성적 근사 모형·경계 한계를 상시 표시 |
| `high3PlanetUniverse/01_solar_planets...` | 위성 수 기준일·출처·갱신 필요 표시 |
| `high3PlanetUniverse/02_planet_atmosphere...` | 목성 1기압 기준면과 내부 열을 온실 효과와 구분 |

## 폴더별 완료 현황

| 폴더 | 완료/전체 |
|---|---:|
| `high2Bio` | 13/13 |
| `high2Chem` | 11/11 |
| `high2Geo` | 16/16 |
| `high2Phy` | 18/18 |
| `high3CellMetabolism` | 8/8 |
| `high3ChemReaction` | 8/8 |
| `high3EMQuantum` | 8/8 |
| `high3EarthSystem` | 8/8 |
| `high3Genetics` | 7/7 |
| `high3MatterEnergy` | 8/8 |
| `high3Mechanics` | 12/12 |
| `high3PlanetUniverse` | 8/8 |

## 파일별 판정

### high2Bio

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_digestive_enzyme_lab_Bio1_Ep03.html` | 개선 | 가열·묽은 염산을 실제 절차처럼 제시하지만 안전 문구 없음 | 보안경·화상/산 취급 주의와 교사 감독 문구 추가 |
| `02_exercise_organ_systems_lab_Bio1_Ep04.html` | 양호 | 원리 227행·compute 455행 대조, 경계/선택 조합 60건에서 예외·비정상 수 없음 | 없음 |
| `03_quadrat_community_lab_Bio1_Ep07.html` | 양호 | 원리 227행·compute 498행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `04_ecosystem_energy_flow_lab_Bio1_Ep06.html` | 양호 | 원리 227행·compute 458행 대조, 경계/선택 조합 5건에서 예외·비정상 수 없음 | 없음 |
| `05_nerve_conduction_lab_Bio1_Ep08.html` | 양호 | 원리 227행·compute 465행 대조, 경계/선택 조합 75건에서 예외·비정상 수 없음 | 없음 |
| `06_synapse_drug_lab_Bio1_Ep09.html` | 양호 | 원리 227행·compute 472행 대조, 경계/선택 조합 12건에서 예외·비정상 수 없음 | 없음 |
| `07_blood_glucose_homeostasis_lab_Bio1_Ep11.html` | 양호 | 원리 227행·compute 469행 대조, 경계/선택 조합 24건에서 예외·비정상 수 없음 | 없음 |
| `08_blood_typing_lab_Bio1_Ep13.html` | 양호 | 원리 227행·compute 458행 대조, 경계/선택 조합 18건에서 예외·비정상 수 없음 | 없음 |
| `09_immune_vaccine_lab_Bio1_Ep12_Ep14.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 6건에서 예외·비정상 수 없음 | 없음 |
| `10_karyotype_lab_Bio1_Ep15.html` | 양호 | 원리 227행·compute 481행 대조, 경계/선택 조합 30건에서 예외·비정상 수 없음 | 없음 |
| `11_meiosis_gamete_diversity_lab_Bio1_Ep16.html` | 양호 | 원리 227행·compute 457행 대조, 경계/선택 조합 40건에서 예외·비정상 수 없음 | 없음 |
| `12_natural_selection_lab_Bio1_Ep17.html` | 양호 | 원리 227행·compute 475행 대조, 경계/선택 조합 8건에서 예외·비정상 수 없음 | 없음 |
| `13_phylogenetic_tree_lab_Bio1_Ep19.html` | 양호 | 원리 227행·compute 478행 대조, 경계/선택 조합 6건에서 예외·비정상 수 없음 | 없음 |

### high2Chem

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_mole_quantity_lab_Chem1_Ep02.html` | 양호 | 원리 227행·compute 459행 대조, 경계/선택 조합 30건에서 예외·비정상 수 없음 | 없음 |
| `02_molar_solution_lab_Chem1_Ep13.html` | 개선 | CuSO₄·5H₂O 및 NaOH 조제 맥락이나 PPE·폐액 안내 없음 | 보안경·장갑, 피부 접촉 방지, 구리 폐액 분리 안내 추가 |
| `03_reaction_stoichiometry_lab_Chem1_Ep03.html` | 개선 | Mg+HCl에서 인화성 H₂ 발생(444~448행), 안전 문구 없음 | 보안경·환기·점화원 차단·소량 실험 안내 추가 |
| `04_water_electrolysis_lab_Chem1_Ep04.html` | 개선 | H₂/O₂를 함께 만드는 전기분해이나 폭발·점화원 주의 없음 | 기체 혼합 금지, 불꽃 금지, 저전압 전원·전원 차단 안내 추가 |
| `05_electronegativity_polarity_lab_Chem1_Ep05.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |
| `06_molecular_shape_lab_Chem1_Ep06-07.html` | 양호 | 원리 227행·compute 464행 대조, 경계/선택 조합 10건에서 예외·비정상 수 없음 | 없음 |
| `07_equilibrium_shift_lab_Chem1_Ep11.html` | 양호 | 원리 227행·compute 458행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `08_equilibrium_constant_lab_Chem1_Ep09-10.html` | 개선 | 황산 촉매·NaOH 적정 절차(243행)이나 부식성 시약 안전 안내 없음 | 보안경·장갑·급랭 시 튐 방지·교사 감독 문구 추가 |
| `09_water_ionization_ph_lab_Chem1_Ep12.html` | 양호 | 원리 227행·compute 460행 대조, 경계/선택 조합 32건에서 예외·비정상 수 없음 | 없음 |
| `10_acid_base_titration_lab_Chem1_Ep15.html` | 개선 | 0.100 M NaOH 뷰렛 적정이나 눈·피부 접촉 및 뷰렛 안전 안내 없음 | 보안경·장갑, 뷰렛 고정, 피부 접촉 시 세척 안내 추가 |
| `11_neutralization_heat_lab_Chem1_Ep14.html` | 개선 | 1.0 M HCl/NaOH 혼합과 발열을 다루나 산·염기·화상 주의 없음 | 보안경·장갑, 천천히 혼합, 용기 과열·튐 주의 추가 |

### high2Geo

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_seawater_density_lab_EarthSci1_Ep01.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 25건에서 예외·비정상 수 없음 | 없음 |
| `02_thermohaline_lab_EarthSci1_Ep02.html` | 양호 | 원리 227행·compute 470행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `03_midlatitude_cyclone_lab_EarthSci1_Ep03.html` | 양호 | 원리 227행·compute 481행 대조, 경계/선택 조합 9건에서 예외·비정상 수 없음 | 없음 |
| `04_typhoon_wind_lab_EarthSci1_Ep04.html` | 양호 | 원리 227행·compute 475행 대조, 경계/선택 조합 60건에서 예외·비정상 수 없음 | 없음 |
| `05_enso_lab_EarthSci1_Ep05.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 8건에서 예외·비정상 수 없음 | 없음 |
| `06_climate_forcing_lab_EarthSci1_Ep06.html` | 양호 | 원리 227행·compute 464행 대조, 경계/선택 조합 90건에서 예외·비정상 수 없음 | 없음 |
| `07_radiometric_age_lab_EarthSci1_Ep08.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 15건에서 예외·비정상 수 없음 | 없음 |
| `08_geologic_time_fossil_lab_EarthSci1_Ep09.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 477행 대조, 경계/선택 조합 12건에서 예외·비정상 수 없음 | 없음 |
| `09_magma_igneous_rock_lab_EarthSci1_Ep10-11.html` | 양호 | 원리 227행·compute 473행 대조, 경계/선택 조합 48건에서 예외·비정상 수 없음 | 없음 |
| `10_geopark_korea_lab_EarthSci1_Ep12.html` | 양호 | 원리 227행·compute 469행 대조, 경계/선택 조합 6건에서 예외·비정상 수 없음 | 없음 |
| `11_eclipse_lab_EarthSci1_Ep13.html` | 양호 | 원리 227행·compute 483행 대조, 경계/선택 조합 150건에서 예외·비정상 수 없음 | 없음 |
| `12_planet_retrograde_lab_EarthSci1_Ep13.html` | 양호 | 원리 227행·compute 473행 대조, 경계/선택 조합 12건에서 예외·비정상 수 없음 | 없음 |
| `13_blackbody_star_lab_EarthSci1_Ep14.html` | 양호 | 원리 227행·compute 461행 대조, 경계/선택 조합 8건에서 예외·비정상 수 없음 | 없음 |
| `14_stellar_evolution_lab_EarthSci1_Ep15.html` | 양호 | 원리 227행·compute 481행 대조, 경계/선택 조합 24건에서 예외·비정상 수 없음 | 없음 |
| `15_galaxy_classification_lab_EarthSci1_Ep16.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 36건에서 예외·비정상 수 없음 | 없음 |
| `16_hubble_law_lab_EarthSci1_Ep17.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 463행 대조, 경계/선택 조합 5건에서 예외·비정상 수 없음 | 없음 |

### high2Phy

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_torque_equilibrium_lab_Physics1_Ep01.html` | 양호 | 원리 225행·compute 463행 대조, 경계/선택 조합 250건에서 예외·비정상 수 없음 | 없음 |
| `02_newton_second_law_lab_Physics1_Ep02.html` | 양호 | 원리 219행·compute 401행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `03_energy_incline_lab_Physics1_Ep04.html` | 양호 | 원리 214행·계산 334행 대조; 사용자 정의 계산 경로와 경계값 정적 확인 | 없음 |
| `04_elastic_energy_lab_Physics1_Ep04.html` | 양호 | 원리 225행·compute 455행 대조, 경계/선택 조합 60건에서 예외·비정상 수 없음 | 없음 |
| `05_momentum_collision_lab_Physics1_Ep03.html` | 양호 | 원리 219행·compute 405행 대조, 경계/선택 조합 375건에서 예외·비정상 수 없음 | 없음 |
| `06_mechanical_to_heat_lab_Physics1_Ep05.html` | 양호 | 원리 225행·compute 450행 대조, 경계/선택 조합 240건에서 예외·비정상 수 없음 | 없음 |
| `07_electric_potential_field_lab_Physics1_Ep07.html` | 양호 | 원리 225행·compute 450행 대조, 경계/선택 조합 80건에서 예외·비정상 수 없음 | 없음 |
| `08_resistor_power_lab_Physics1_Ep08.html` | 양호 | 원리 225행·compute 458행 대조, 경계/선택 조합 128건에서 예외·비정상 수 없음 | 없음 |
| `09_capacitor_energy_lab_Physics1_Ep09.html` | 양호 | 원리 225행·compute 449행 대조, 경계/선택 조합 12건에서 예외·비정상 수 없음 | 없음 |
| `10_magnetic_materials_lab_Physics1_Ep10.html` | 양호 | 원리 225행·compute 459행 대조, 경계/선택 조합 28건에서 예외·비정상 수 없음 | 없음 |
| `11_current_magnetic_force_lab_Physics1_Ep11.html` | 양호 | 원리 225행·compute 451행 대조, 경계/선택 조합 90건에서 예외·비정상 수 없음 | 없음 |
| `12_electromagnetic_induction_lab_Physics1_Ep12.html` | 양호 | 원리 217행·계산 None행 대조; 사용자 정의 계산 경로와 경계값 정적 확인 | 없음 |
| `13_convex_lens_image_lab_Physics1_Ep14.html` | 양호 | 원리 225행·compute 452행 대조, 경계/선택 조합 15건에서 예외·비정상 수 없음 | 없음 |
| `14_double_slit_interference_lab_Physics1_Ep13.html` | 개선 | 레이저 켜기 조작(262행)이나 눈 노출 방지 문구 없음 | 빔을 눈·반사면에 향하지 말고 저출력 교육용 레이저 사용 안내 |
| `15_photoelectric_effect_lab_Physics1_Ep15.html` | 양호 | 원리 219행·compute 407행 대조, 경계/선택 조합 96건에서 예외·비정상 수 없음 | 없음 |
| `16_atomic_spectrum_lab_Physics1_Ep16.html` | 양호 | 원리 225행·compute 471행 대조, 경계/선택 조합 20건에서 예외·비정상 수 없음 | 없음 |
| `17_pn_diode_lab_Physics1_Ep17.html` | 양호 | 원리 225행·compute 459행 대조, 경계/선택 조합 10건에서 예외·비정상 수 없음 | 없음 |
| `18_special_relativity_lab_Physics1_Ep18.html` | 양호 | 원리 225행·compute 459행 대조, 경계/선택 조합 10건에서 예외·비정상 수 없음 | 없음 |

### high3CellMetabolism

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_cell_organelle_lab_CellMetab_Ep03.html` | 양호 | 원리 227행·compute 469행 대조, 경계/선택 조합 20건에서 예외·비정상 수 없음 | 없음 |
| `02_membrane_transport_lab_CellMetab_Ep05.html` | 양호 | 원리 227행·compute 474행 대조, 경계/선택 조합 200건에서 예외·비정상 수 없음 | 없음 |
| `03_cell_cycle_lab_Bio1_Ep16.html` | 개선 | 양파 뿌리를 염산 처리·염색(471행)하나 안전·폐액 안내 없음 | 산·염색액 PPE, 교사 감독, 폐액 처리 안내 추가 |
| `04_enzyme_kinetics_lab_CellMetab_Ep08-09.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 1350건에서 예외·비정상 수 없음 | 없음 |
| `05_cellular_respiration_lab_CellMetab_Ep12-13.html` | 양호 | 원리 227행·compute 465행 대조, 경계/선택 조합 18건에서 예외·비정상 수 없음 | 없음 |
| `06_yeast_fermentation_lab_CellMetab_Ep14.html` | 양호 | 원리 227행·compute 467행 대조, 경계/선택 조합 160건에서 예외·비정상 수 없음 | 없음 |
| `07_photosynthesis_rate_lab_CellMetab_Ep16.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 72건에서 예외·비정상 수 없음 | 없음 |
| `08_photo_pigment_lab_CellMetab_Ep15.html` | 양호 | 원리 227행·compute 470행 대조, 경계/선택 조합 288건에서 예외·비정상 수 없음 | 없음 |

### high3ChemReaction

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_reaction_rate_lab_MatterEnergy_Ep13-14.html` | 개선 | 티오황산염+염산 반응은 SO₂가 생기나 228·263행에 환기 주의 없음 | 후드/충분한 환기, 소량 사용, 흡입 금지·보안경 안내 추가 |
| `02_weak_acid_ka_lab_ChemReaction_Ep02.html` | 개선 | 247행은 약산이라 같은 농도 HCl보다 pH가 높아 “마실 수 있다”고 단순 인과화 | 음용 안전성은 산의 세기뿐 아니라 농도·독성·불순물에 달린다고 수정 |
| `03_titration_buffer_lab_ChemReaction_Ep03_Ep05.html` | 개선 | HCl·NaOH 실제 적정 맥락이나 부식성 시약 안전 문구 없음 | 보안경·장갑·뷰렛 고정·피부 접촉 시 세척 안내 추가 |
| `04_solubility_ksp_lab_ChemReaction.html` | 양호 | 원리 227행·compute 477행 대조, 경계/선택 조합 150건에서 예외·비정상 수 없음 | 없음 |
| `05_redox_number_lab_ChemReaction_Ep06.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 12건에서 예외·비정상 수 없음 | 없음 |
| `06_galvanic_cell_lab_ChemReaction_Ep08.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 461행 대조, 경계/선택 조합 147건에서 예외·비정상 수 없음 | 없음 |
| `07_electrolysis_plating_lab_ChemReaction_Ep09.html` | 개선 | 산성 전해질과 H₂/O₂ 발생을 다루나 전기·기체 안전 안내 없음 | 저전압, 전원 차단, 환기, 점화원 차단, 전해질 PPE 안내 |
| `08_fuel_cell_lab_ChemReaction_Ep10.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 36건에서 예외·비정상 수 없음 | 없음 |

### high3EMQuantum

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_coulomb_field_lab_EMQuantum_Ep01.html` | 양호 | 원리 227행·compute 466행 대조, 경계/선택 조합 192건에서 예외·비정상 수 없음 | 없음 |
| `02_dielectric_capacitor_lab_EMQuantum_Ep02.html` | 양호 | 원리 227행·compute 461행 대조, 경계/선택 조합 108건에서 예외·비정상 수 없음 | 없음 |
| `03_current_bfield_lab_EMQuantum_Ep03.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 432건에서 예외·비정상 수 없음 | 없음 |
| `04_lorentz_motion_lab_EMQuantum_Ep04.html` | 양호 | 원리 227행·compute 463행 대조, 경계/선택 조합 64건에서 예외·비정상 수 없음 | 없음 |
| `05_transformer_lab_EMQuantum_Ep05.html` | 양호 | 원리 227행·compute 456행 대조, 경계/선택 조합 216건에서 예외·비정상 수 없음 | 없음 |
| `06_matter_wave_lab_EMQuantum_Ep13.html` | 양호 | 원리 227행·compute 463행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `07_photon_duality_lab_EMQuantum_Ep13.html` | 양호 | 원리 227행·compute 479행 대조, 경계/선택 조합 32건에서 예외·비정상 수 없음 | 없음 |
| `08_laser_energy_level_lab_EMQuantum_Ep12.html` | 양호 | 원리 227행·compute 470행 대조, 경계/선택 조합 48건에서 예외·비정상 수 없음 | 없음 |

### high3EarthSystem

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_earth_formation_lab_EarthSystem_Ep01.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 48건에서 예외·비정상 수 없음 | 없음 |
| `02_seismic_interior_lab_EarthSystem_Ep05.html` | 양호 | 원리 227행·compute 465행 대조, 경계/선택 조합 18건에서 예외·비정상 수 없음 | 없음 |
| `03_seafloor_spreading_lab_EarthSystem_Ep03.html` | 양호 | 원리 227행·compute 463행 대조, 경계/선택 조합 45건에서 예외·비정상 수 없음 | 없음 |
| `04_ekman_transport_lab_EarthSystem_Ep06.html` | 양호 | 원리 227행·compute 474행 대조, 경계/선택 조합 64건에서 예외·비정상 수 없음 | 없음 |
| `05_atmospheric_wind_lab_EarthSystem_Ep14.html` | 양호 | 원리 227행·compute 465행 대조, 경계/선택 조합 72건에서 예외·비정상 수 없음 | 없음 |
| `06_global_circulation_lab_EarthSystem_Ep15.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 14건에서 예외·비정상 수 없음 | 없음 |
| `07_precipitation_lab_EarthSystem_Ep12.html` | 양호 | 원리 227행·compute 467행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |
| `08_carbon_cycle_lab_EarthSystem_Ep02.html` | 양호 | 원리 227행·compute 477행 대조, 경계/선택 조합 56건에서 예외·비정상 수 없음 | 없음 |

### high3Genetics

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_dna_replication_lab_Genetics_Ep05_Ep07.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 48건에서 예외·비정상 수 없음 | 없음 |
| `02_transcription_translation_lab_Genetics_Ep08-09.html` | 양호 | 원리 227행·compute 491행 대조, 경계/선택 조합 15건에서 예외·비정상 수 없음 | 없음 |
| `03_gene_regulation_lab_Genetics_Ep10.html` | 양호 | 원리 227행·compute 466행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `04_mendel_cross_lab_Genetics_Ep01.html` | 양호 | 원리 227행·compute 488행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `05_gene_linkage_lab_Genetics.html` | 양호 | 원리 227행·compute 466행 대조, 경계/선택 조합 16건에서 예외·비정상 수 없음 | 없음 |
| `06_human_pedigree_lab_Genetics_Ep02.html` | 양호 | 원리 227행·compute 477행 대조, 경계/선택 조합 120건에서 예외·비정상 수 없음 | 없음 |
| `07_chromosome_mutation_lab_Genetics_Ep04.html` | 양호 | 원리 227행·compute 470행 대조, 경계/선택 조합 72건에서 예외·비정상 수 없음 | 없음 |

### high3MatterEnergy

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_reaction_enthalpy_lab_MatterEnergy_Ep08.html` | 오류 | 원리 설명 234행은 중화열 −57.3 kJ/mol·ΔT≈6.9 ℃, 계산 배열 447행은 −56.1 kJ/mol이며 열량계 열용량까지 넣어 서로 불일치 | 한 기준값으로 통일하고 같은 질량·열용량 가정으로 예시 ΔT를 다시 계산 |
| `02_hess_law_lab_MatterEnergy_Ep09.html` | 개선 | 고체 NaOH를 물/산에 넣는 경로를 제시하나 강한 발열·부식성 주의 없음 | NaOH를 소량씩 넣고 보안경·장갑·비산/화상 주의 추가 |
| `03_gibbs_energy_lab_MatterEnergy_Ep10.html` | 양호 | 원리 227행·compute 467행 대조, 경계/선택 조합 30건에서 예외·비정상 수 없음 | 없음 |
| `04_ideal_gas_law_lab_MatterEnergy_Ep01.html` | 양호 | 원리 227행·compute 464행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |
| `05_intermolecular_force_lab_MatterEnergy_Ep03.html` | 양호 | 원리 227행·compute 474행 대조, 경계/선택 조합 30건에서 예외·비정상 수 없음 | 없음 |
| `06_phase_diagram_lab_MatterEnergy_Ep03.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 485행 대조, 경계/선택 조합 126건에서 예외·비정상 수 없음 | 없음 |
| `07_solution_concentration_lab_MatterEnergy_Ep07.html` | 양호 | 원리 227행·compute 459행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |
| `08_colligative_property_lab_MatterEnergy_Ep06-07.html` | 양호 | 원리 227행·compute 461행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |

### high3Mechanics

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_force_vector_lab_MechEnergy_Ep01.html` | 양호 | 원리 227행·compute 458행 대조, 경계/선택 조합 2500건에서 예외·비정상 수 없음 | 없음 |
| `02_projectile_motion_lab_MechEnergy_Ep02.html` | 양호 | 원리 227행·compute 464행 대조, 경계/선택 조합 400건에서 예외·비정상 수 없음 | 없음 |
| `03_circular_motion_lab_MechEnergy_Ep03.html` | 양호 | 원리 227행·compute 453행 대조, 경계/선택 조합 100건에서 예외·비정상 수 없음 | 없음 |
| `04_satellite_orbit_lab_MechEnergy_Ep04.html` | 양호 | 원리 227행·compute 465행 대조, 경계/선택 조합 80건에서 예외·비정상 수 없음 | 없음 |
| `05_escape_velocity_lab_MechEnergy_Ep05.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 60건에서 예외·비정상 수 없음 | 없음 |
| `06_gravity_time_lab_MechEnergy_Ep06.html` | 양호 | 원리 227행·compute 466행 대조, 경계/선택 조합 18건에서 예외·비정상 수 없음 | 없음 |
| `07_gas_thermo_lab_MechEnergy_Ep08-09.html` | 양호 | 원리 227행·compute 481행 대조, 경계/선택 조합 108건에서 예외·비정상 수 없음 | 없음 |
| `08_heat_engine_lab_MechEnergy_Ep10.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 144건에서 예외·비정상 수 없음 | 없음 |
| `09_wave_boundary_lab_MechEnergy_Ep13.html` | 양호 | 원리 227행·compute 462행 대조, 경계/선택 조합 36건에서 예외·비정상 수 없음 | 없음 |
| `10_sound_interference_lab_MechEnergy_Ep15.html` | 양호 | 원리 227행·compute 464행 대조, 경계/선택 조합 432건에서 예외·비정상 수 없음 | 없음 |
| `11_doppler_effect_lab_MechEnergy_Ep14.html` | 양호 | 원리 227행·compute 461행 대조, 경계/선택 조합 90건에서 예외·비정상 수 없음 | 없음 |
| `12_standing_wave_lab_MechEnergy_Ep16.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 540건에서 예외·비정상 수 없음 | 없음 |

### high3PlanetUniverse

| 파일 | 판정 | 근거 | 제안 수정 |
|---|---|---|---|
| `01_solar_planets_lab_PlanetUniverse_Ep03.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 464행 대조, 경계/선택 조합 24건에서 예외·비정상 수 없음 | 없음 |
| `02_planet_atmosphere_lab_PlanetUniverse_Ep05.html` | 양호(기존 오류 수정 확인) | 원리 227행·compute 470행 대조, 경계/선택 조합 6건에서 예외·비정상 수 없음 | 없음 |
| `03_exoplanet_detection_lab_PlanetUniverse_Ep05.html` | 양호 | 원리 227행·compute 469행 대조, 경계/선택 조합 48건에서 예외·비정상 수 없음 | 없음 |
| `04_solar_observation_lab_PlanetUniverse_Ep06.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 360건에서 예외·비정상 수 없음 | 없음 |
| `05_star_formation_lab_PlanetUniverse_Ep12.html` | 양호 | 원리 227행·compute 471행 대조, 경계/선택 조합 96건에서 예외·비정상 수 없음 | 없음 |
| `06_cosmic_distance_lab_PlanetUniverse_Ep07.html` | 양호 | 원리 227행·compute 477행 대조, 경계/선택 조합 24건에서 예외·비정상 수 없음 | 없음 |
| `07_dark_matter_lab_PlanetUniverse_Ep13.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 36건에서 예외·비정상 수 없음 | 없음 |
| `08_bigbang_evidence_lab_EarthSci1_Ep17.html` | 양호 | 원리 227행·compute 468행 대조, 경계/선택 조합 288건에서 예외·비정상 수 없음 | 없음 |

## 최종 완료 표시

- **검토 완료 파일 수 / 전체 파일 수: 125 / 125**
- 원본 HTML은 수정하지 않았다.
- Google Drive에는 업로드하지 않았다.
