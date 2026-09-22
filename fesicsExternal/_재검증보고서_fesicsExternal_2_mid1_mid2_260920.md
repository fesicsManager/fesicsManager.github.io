# 재검증보고서 — fesicsExternal 배치 2 (중1·중2 91 HTML)

- 검증일: 2026-09-20
- 대상: `2_mid1_mid2_91html.zip`
- 범위: 11개 폴더, HTML 91개 (중1 31개, 중2 기본·심화 60개)
- 판정: **오류 2 / 개선 15 / 양호 74**
- 무결성: `_MANIFEST_SHA256.tsv`와 HTML 91개 SHA-256 전부 일치
- Google Drive 업로드: 하지 않음

## 결론

전 파일의 화면 설명, 계산식, 퀴즈 정답·오차 허용 범위, 단위, 슬라이더 경계값, 기록 중복 방지, 탭 전환, 리셋, 연속 클릭 방지/애니메이션 상태 변수를 코드 흐름으로 대조했다. 기존 2026-09-12 지적 64건(오류 23·개선 41) 중 **62건은 반영 완료**, 2건은 부분 반영 상태다.

1. **내용 오류 2건**
   - `milddle1BioGeo/07_blackbody_lab.html`: 불꽃색 설명과 퀴즈 해설이 서로 모순.
   - `milddle2Chem/10_matter_composition_summary_lab.html`: 원자·분자·이온·화합물을 단일 크기 계층으로 정답 처리.
2. **안전·표현 개선 15건**
   - 주로 알코올램프/고온, 에탄올 증류, 아이오딘·침, Pb²⁺·Ba²⁺·Ag⁺ 용액, 산 용액, 고전류 니크롬선의 실제 재현 가능 장면에 안전 문구가 빠져 있다.
3. 나머지 **74개는 양호**하다. 임의 함수·대표값은 현재 대부분 “교육용 모형/근사/조건”으로 상시 표시되어 이전의 오개념 위험이 크게 줄었다.

## 외부 기준 확인

변동 가능한 행성 위성 수는 NASA 최신 페이지와 대조했다. 현재 HTML의 목성 115(2026년 8월 기준), 천왕성 29(2026년 8월 기준), 해왕성 16은 일치한다. 토성 293도 동봉 기준과 현재 NASA 안내에 맞게 유지되어 있다.

- NASA Jupiter Moons: https://science.nasa.gov/jupiter/jupiter-moons/
- NASA Saturn Moons: https://science.nasa.gov/saturn/moons/
- NASA Uranus Moons: https://science.nasa.gov/uranus/moons/
- NASA Neptune Moons: https://science.nasa.gov/neptune/moons/

## 파일별 판정

| 파일 | 판정(오류/개선/양호) | 근거(줄 번호 또는 코드·문구) | 제안 수정 |
|---|---|---|---|
| `milddle1BioGeo/01_stimulus_response_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/02_diffusion_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/03_scale_observation_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/04_classification_lab.html` | 개선 | 종을 “자연에서 교배해 생식 가능한 자손”으로 단일 정의(원리 카드)함. 중1 수준에는 유용하지만 무성생식 생물·화석·잡종 예외가 빠짐. | “주로 유성생식 생물에 적용되는 생물학적 종 개념”이라는 한정 한 문장 추가. |
| `milddle1BioGeo/05_habitat_extinction_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/06_orbit_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/07_blackbody_lab.html` | 오류 | 본문 208·257행은 불꽃색을 온도만으로 단정할 수 없다고 올바르게 설명하지만, 684행 퀴즈 해설은 “가장 뜨거운 속불꽃이 푸르게 보인다”고 다시 단정해 내부 모순. | 퀴즈 해설의 모닥불 문장을 삭제하고 “별의 흑체색과 불꽃색은 같은 기준으로 비교할 수 없다”로 교체. |
| `milddle1BioGeo/08_exoplanet_density_lab.html` | 양호 | 206행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1BioGeo/09_planet_survey_lab.html` | 개선 | 위성 수 115·293·29·16은 2026-09 NASA 기준과 일치. 다만 퀴즈 해설이 위성 수를 행성 질량 하나로 설명함. | 힐 구, 태양과의 거리, 충돌·포획 역사, 관측 편향도 위성 수에 영향을 준다고 보완. |
| `milddle1BioGeo/10_solar_system_exploration_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/01_states_of_matter_lab.html` | 양호 | 180행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/02_state_change_types_lab.html` | 개선 | 드라이아이스·나프탈렌을 생활 예로 제시하지만 실제 취급 시 동상·환기·섭취 위험 안내 없음. | 가상 실험임을 명시하고 실제 취급은 보호장갑·환기·교사 감독 문구 추가. |
| `milddle1Chem/03_heat_absorption_release_lab.html` | 개선 | 알코올램프·100℃ 이상 가열 장면이 있으나 화상·화재 안전 문구 없음. | 보안경, 내열장갑, 교사 감독, 밀폐 가열 금지 문구 추가. |
| `milddle1Chem/04_heating_curve_lab.html` | 양호 | 138행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/05_phase_change_applications_lab.html` | 양호 | 149행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/06_gas_particles_pressure_lab.html` | 양호 | 157행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/07_boyles_law_lab.html` | 양호 | 292행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/08_charles_law_lab.html` | 개선 | 알코올램프 가열 조작을 보여 주지만 화재·뜨거운 유리·밀폐 용기 위험 안내 없음. | 실제 재현 금지 또는 교사 감독·밀폐 금지·화상 주의 추가. |
| `milddle1Chem/09_gas_diffusion_lab.html` | 양호 | 196행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Chem/10_gas_properties_summary_lab.html` | 개선 | 알코올램프 불꽃이 커지는 장면을 “실제로 열을 가하는 모습”이라 표현하지만 안전 문구 없음. | 가상 화면임을 명확히 하고 실제 불꽃 실험 안전 문구 추가. |
| `milddle1Phy/01_temperature_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/02_heat_transfer_lab.html` | 개선 | 가열된 막대의 50℃ 도달 활동에 화상 주의가 없음. 계산식의 경계 조건·근사 표시는 양호. | 실물 실험 시 맨손 접촉 금지·집게/내열장갑·냉각 후 정리 추가. |
| `milddle1Phy/03_thermal_equilibrium_lab.html` | 양호 | 203행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/04_specific_heat_thermal_expansion_lab.html` | 개선 | 금속 막대 가열 장면에 화상·열원 안전 안내 없음. | 가상 실험임을 밝히고 실제 가열은 교사 감독·보호구 사용 문구 추가. |
| `milddle1Phy/05_insulation_lab.html` | 개선 | 뜨거운 물과 보온병 비교를 실제로 재현하기 쉬우나 화상 주의가 없음. | 끓는 물 대신 안전한 온도 범위 사용, 넘침·화상 주의 추가. |
| `milddle1Phy/06_force_representation_lab.html` | 양호 | 204행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/07_gravity_weight_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/08_elasticity_friction_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/09_buoyancy_lab.html` | 양호 | 204행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/10_pressure_lab.html` | 양호 | 203행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle1Phy/11_wall_insulation_lab.html` | 양호 | 319행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/01_photosynthesis_lab.html` | 양호 | 214행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/02_plant_tissue_lab.html` | 양호 | 218행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/03_water_transport_lab.html` | 양호 | 214행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/04_transpiration_lab.html` | 양호 | 215행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/05_photosynthesis_use_lab.html` | 양호 | 213행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/06_digestion_lab.html` | 양호 | 217행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/07_circulation_lab.html` | 양호 | 214행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/08_respiration_lab.html` | 양호 | 215행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/09_excretion_lab.html` | 양호 | 217행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Bio/10_integration_lab.html` | 양호 | 216행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2BioAdv/01_light_limiting_factor_lab.html` | 양호 | 181행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2BioAdv/04_transpiration_vaseline_lab.html` | 양호 | 171행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2BioAdv/06_enzyme_temperature_lab.html` | 개선 | 침·아이오딘 용액·물중탕을 실제 실험처럼 설명하나 체액 위생, 아이오딘 섭취 금지, 가열 안전 문구가 없음. | 개인별 도구 사용, 입에 넣지 않기, 아이오딘 피부·눈 접촉 주의, 교사 감독 문구 추가. |
| `milddle2BioAdv/07_pulse_recovery_lab.html` | 양호 | 172행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2BioAdv/09_reabsorption_lab.html` | 양호 | 171행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/01_pure_substance_mixture_lab.html` | 양호 | 224행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/02_density_lab.html` | 양호 | 224행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/03_solubility_melting_boiling_lab.html` | 양호 | 223행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/04_separation_density_distillation_lab.html` | 개선 | 에탄올–물 증류를 설명하지만 인화성 증기와 화기 사용 금지 안내 없음. | 에탄올 증류는 화기 금지·환기·교사 감독, 가열판 사용 등 안전 문구 추가. |
| `milddle2Chem/05_recrystallization_chromatography_lab.html` | 개선 | 뜨거운 용액과 전개액을 쓰는 실제 활동으로 확장 가능하나 화상·용매 안전 안내 없음. | 전개액 종류에 따른 환기/화기 금지와 뜨거운 용액 취급 주의 추가. |
| `milddle2Chem/06_elements_atoms_lab.html` | 양호 | 228행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/07_molecules_lab.html` | 양호 | 226행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/08_ions_lab.html` | 양호 | 225행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Chem/09_precipitation_reaction_lab.html` | 개선 | Ag⁺·Ba²⁺·Pb²⁺ 용액을 선택 가능하고 “실제 앙금 반응”이라 안내하지만 은·바륨·납 염의 유해성 및 폐액 처리 안내 없음. | 학생 임의 재현 금지, 보안경·장갑·교사 감독, 중금속 폐액 전용 수거 문구 추가. |
| `milddle2Chem/10_matter_composition_summary_lab.html` | 오류 | 335~350·938~944행이 “원자 → 분자·이온 → 화합물”을 크기 순서의 정답으로 처리하고 “원자가 모여 이온”이라고 설명. 이온은 원자의 전자 수가 변한 입자이며 분자보다 반드시 크거나 작은 단계가 아니고, 화합물도 크기 단계가 아님. | 계층형 문항을 삭제. “원자 → (결합) 분자”, “원자 → (전자 이동) 이온”, “분자 화합물/이온 화합물”의 가지 구조로 교체. |
| `milddle2ChemAdv/02_density_float_lab.html` | 양호 | 209행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2ChemAdv/03_solubility_precipitation_lab.html` | 양호 | 183행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2ChemAdv/06_atomic_number_lab.html` | 양호 | 185행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2ChemAdv/07_molecule_count_lab.html` | 양호 | 181행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2ChemAdv/08_ion_formula_lab.html` | 양호 | 178행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/01_earth_internal_structure.html` | 양호 | 176행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/02_plate_tectonics.html` | 양호 | 178행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/03_earthquake_volcano.html` | 양호 | 181행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/04_rock_cycle.html` | 양호 | 176행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/05_weathering_soil.html` | 개선 | 산성비와 H⁺ 용해 활동이 실제 산 용액 사용으로 이어질 수 있으나 눈·피부 보호와 폐액 안내 없음. | 묽은 산도 교사 감독, 보안경·장갑, 피부 접촉 시 세척, 폐액 처리 문구 추가. |
| `milddle2Geo/06_star_brightness_color.html` | 양호 | 178행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/07_star_motion.html` | 양호 | 176행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/08_galaxy.html` | 양호 | 177행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/09_universe_expansion.html` | 양호 | 175행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Geo/10_space_exploration.html` | 양호 | 177행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2GeoAdv/02_plate_speed_lab.html` | 양호 | 177행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2GeoAdv/03_earthquake_energy_lab.html` | 양호 | 177행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2GeoAdv/06_star_magnitude_lab.html` | 양호 | 170행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2GeoAdv/07_diurnal_annual_motion_lab.html` | 양호 | 175행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2GeoAdv/09_hubble_law_lab.html` | 양호 | 174행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/01_light_straight_line_lab.html` | 양호 | 171행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/02_light_reflection_lab.html` | 양호 | 182행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/03_refraction_lens_lab.html` | 양호 | 182행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/04_wave_properties_lab.html` | 양호 | 174행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/05_sound_lab.html` | 양호 | 173행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/06_static_electricity_lab.html` | 양호 | 175행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/07_ohms_law_lab.html` | 개선 | 20 V·2 Ω=10 A, 100 W로 니크롬선이 벌겋게 달아오르는 예를 제시하지만 실제 연결 금지·화상·과전류 경고 없음. | 저전압 전원과 전류 제한 사용, 20 V 조건 재현 금지, 발열체 접촉 금지 문구 추가. |
| `milddle2Phy/08_electromagnetism_lab.html` | 양호 | 173행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/09_electromagnetic_induction_lab.html` | 양호 | 170행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2Phy/10_electricity_magnetism_summary_lab.html` | 양호 | 182행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2PhyAdv/03_lens_image_cases_lab.html` | 양호 | 181행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2PhyAdv/04_wave_speed_lab.html` | 양호 | 184행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2PhyAdv/07_series_parallel_lab.html` | 양호 | 182행: 📌 실험 모형과 실제의 차이 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2PhyAdv/08_electromagnet_strength_lab.html` | 양호 | 179행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |
| `milddle2PhyAdv/09_induction_direction_lab.html` | 양호 | 182행: 🧮 이 실험의 계산 방법 | 수식·정답·단위·모형 한계 및 입력/기록/초기화 코드 흐름에서 추가 수정 필요 없음. |

## 조작 결과 검증 메모

- 91개 모두 HTML/인라인 스크립트를 정적으로 추적했다. 입력의 `min/max/step`, 데이터 기록 조건, 같은 조건 중복 방지, 부족한 데이터 처리, 탭 전환, 초기화 후 배열·선택값·그래프 상태, 퀴즈 판정 분기를 확인했다.
- 기존 자동검사 결과(JS 구문, 중복 ID, 고정 DOM 참조, viewport/@media)는 동봉 안내에 따라 재판정 대상에서 제외했으나, 내용검증 중 관련 코드가 보이는 경우 함께 확인했다.
- **실제 브라우저 클릭 검사는 수행하지 못했다.** 검증 환경에 실행 가능한 Chromium이 없어 자동 클릭 순회가 시작되지 않았다. 따라서 “모든 조작 결과”는 소스 코드의 이벤트·상태 흐름을 전수 추적한 결과이며, 픽셀 렌더링·터치·실시간 타이밍은 별도 실제 브라우저 확인이 필요하다.

## 기존 09-12 지적 반영 상태

- 완전 반영: **62/64건**
- 부분 반영: **2/64건** (`milddle1BioGeo/07_blackbody_lab.html`, `milddle2Chem/10_matter_composition_summary_lab.html`)
- 기술 지적(없는 DOM 참조, 중복 ID·스크립트, 입력 접근성 이름)은 현재 파일에서 해소된 상태임을 코드에서 확인했다.

## 검토 완료 수

**검토 완료 91 / 전체 91 HTML**
