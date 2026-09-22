# fesicsLabs 웹 실험 파일 정밀 검증 보고서

- 검증일: 2026-09-21
- 대상 폴더: `G:\내 드라이브\Misodle Software\fesicsExternal\fesicsLabs`
- 대상: HTML 195개 (`index.html` 1개 + 개별 실험 194개)

## 최종 판정

**배포 차단 수준의 구조·스크립트 오류는 발견되지 않았습니다.**

195개 전부를 원본으로 내려받아 파일별 검사를 수행했습니다. `index.html`에는 개별 실험 194개 링크가 있으며, 누락 링크·중복 링크·고아 파일이 모두 0개입니다. 개별 실험은 공통 템플릿을 쓰되 주제별 계산식·데이터·그래프 코드가 따로 포함되어 있습니다.

다만 이 판정은 소스 정적 검사와 격리된 실행 시뮬레이션을 중심으로 한 것입니다. 실제 Chrome 화면에서의 픽셀 단위 겹침·기기별 글꼴 차이·터치 감도는 별도 실기기 회귀 검사가 필요합니다.

## 검사 결과 요약

| 검사 항목 | 결과 |
|---|---:|
| 원본 확보 및 파일 수 대조 | 195/195 정상 |
| `index.html` 링크 수 | 194개 |
| 링크 대상 누락 | 0개 |
| 인덱스에 없는 고아 실험 파일 | 0개 |
| JavaScript 문법 오류 | 0개 |
| 초기화 실행 오류 | 0개 |
| 중복 HTML `id` | 0개 |
| 코드에서 참조하지만 존재하지 않는 고정 DOM `id` | 0개 |
| `lang="ko"` 누락 | 0개 |
| 모바일 viewport 메타 누락 | 0개 |
| 외부 CDN·원격 스크립트 의존 | 0개 |
| 명백한 미완성 표기(TODO/FIXME/placeholder) | 0개 |

## 세부 검증 내용

1. **파일·인덱스 무결성**
   - `index.html`이 실험 HTML 194개를 정확히 한 번씩 연결합니다.
   - 링크된 파일이 실제 폴더에 모두 존재합니다.

2. **HTML·접근성 기본 구조**
   - 한국어 문서 언어, viewport, 문서 제목, 고유 ID 구조를 전수 검사했습니다.
   - 탭·버튼·슬라이더·캔버스의 기본 요소와 참조 관계를 확인했습니다.

3. **JavaScript·상호작용 경로**
   - 모든 내장 스크립트를 파일별로 독립 컴파일해 문법 오류를 검사했습니다.
   - 초기 화면 구성, 제어부 생성, 계산 실행, 기록 추가, 기록 삭제, 검증 탭 전환 경로를 격리 실행했습니다.
   - 194개 실험의 공통 실행 경로에서 초기화 중단이나 계산 예외가 나오지 않았습니다.

4. **과학 데이터·표시 일관성**
   - 주제명, 단위 표기, 슬라이더 범위, 결과표 열, 그래프 축·범례 생성 코드의 구조적 일관성을 검사했습니다.
   - 계산 결과에 `NaN`, `undefined`, `Infinity`가 노출되는 명백한 경로와 미완성 문구는 발견되지 않았습니다.

## 참고 관찰(오류 아님)

아래 10개는 브라우저 탭 제목과 화면 큰 제목의 표현이 조금 다릅니다. 내용상 충돌은 아니며, 화면 제목을 더 구체적으로 쓴 경우라 수정 필수 항목에서 제외했습니다.

- `capacitor_energy_hs2_Physics1_Ep09.html`
- `convex_lens_image_hs2_Physics1_Ep14.html`
- `current_magnetic_force_hs2_Physics1_Ep11.html`
- `double_slit_interference_hs2_Physics1_Ep13.html`
- `elastic_energy_hs2_Physics1_Ep04.html`
- `electric_potential_field_hs2_Physics1_Ep07.html`
- `magnetic_materials_hs2_Physics1_Ep10.html`
- `photoelectric_effect_hs2_Physics1_Ep15.html`
- `pn_diode_hs2_Physics1_Ep17.html`
- `special_relativity_hs2_Physics1_Ep18.html`

## 범위별 수량

| 구분 | 파일 수 |
|---|---:|
| 고2 개별 실험 | 58 |
| 고3 개별 실험 | 136 |
| 통합 인덱스 | 1 |
| 합계 | 195 |

## 파일별 검증 목록

아래 파일은 모두 원본 존재, 인덱스 연결, JavaScript 문법, 초기화 실행, DOM 참조 검사를 통과했습니다.

1. `ac_resonance_em_hs3_EMQuantum_Ep06.html` — 통과
2. `acid_base_titration_chem_hs2_Chem1_Ep15.html` — 통과
3. `atmospheric_wind_gs_hs3_EarthSystem_Ep14.html` — 통과
4. `atomic_spectrum_hs2_Physics1_Ep16.html` — 통과
5. `aurora_gs_hs3_EMQuantum_Ep04.html` — 통과
6. `battery_cr_hs3_ChemReaction_Ep10.html` — 통과
7. `bigbang_evidence_pu_hs3_EarthSci1_Ep17.html` — 통과
8. `binary_star_pu_hs3_PlanetUniverse_Ep09.html` — 통과
9. `biomolecule_test_cm_hs3_CellMetab_Ep01-02.html` — 통과
10. `black_hole_pu_hs3_MechEnergy_Ep06.html` — 통과
11. `blackbody_star_earth_hs2_EarthSci1_Ep14.html` — 통과
12. `blood_glucose_homeostasis_bio_hs2_Bio1_Ep11.html` — 통과
13. `blood_typing_bio_hs2_Bio1_Ep13.html` — 통과
14. `bond_energy_me_hs3_MatterEnergy_Ep08.html` — 통과
15. `bronsted_acid_cr_hs3_ChemReaction_Ep01.html` — 통과
16. `buoyancy_dyn_hs3_MechEnergy.html` — 통과
17. `capacitor_energy_hs2_Physics1_Ep09.html` — 통과
18. `carbon_cycle_gs_hs3_EarthSystem_Ep02.html` — 통과
19. `cell_cycle_cm_hs3_Bio1_Ep16.html` — 통과
20. `cell_cycle_control_cm_hs3_Bio1_Ep16.html` — 통과
21. `cell_organelle_cm_hs3_CellMetab_Ep03.html` — 통과
22. `cell_signaling_cm_hs3_CellMetab.html` — 통과
23. `cellular_respiration_cm_hs3_CellMetab_Ep12-13.html` — 통과
24. `centrifuge_cm_hs3_CellMetab_Ep03.html` — 통과
25. `chromosome_mutation_gn_hs3_Genetics_Ep04.html` — 통과
26. `circular_motion_dyn_hs3_MechEnergy_Ep03.html` — 통과
27. `climate_forcing_earth_hs2_EarthSci1_Ep06.html` — 통과
28. `colligative_property_me_hs3_MatterEnergy_Ep06-07.html` — 통과
29. `convex_lens_image_hs2_Physics1_Ep14.html` — 통과
30. `corrosion_cr_hs3_IntegSci2_Change_Ep05.html` — 통과
31. `cosmic_distance_pu_hs3_PlanetUniverse_Ep07.html` — 통과
32. `coulomb_field_em_hs3_EMQuantum_Ep01.html` — 통과
33. `crystal_structure_me_hs3_MatterEnergy_Ep04.html` — 통과
34. `current_bfield_em_hs3_EMQuantum_Ep03.html` — 통과
35. `current_magnetic_force_hs2_Physics1_Ep11.html` — 통과
36. `dark_matter_pu_hs3_PlanetUniverse_Ep13.html` — 통과
37. `dielectric_capacitor_em_hs3_EMQuantum_Ep02.html` — 통과
38. `digestive_enzyme_bio_hs2_Bio1_Ep03.html` — 통과
39. `dna_replication_gn_hs3_Genetics_Ep05_Ep07.html` — 통과
40. `dna_sequencing_gn_hs3_Genetics_Ep13.html` — 통과
41. `doppler_effect_dyn_hs3_MechEnergy_Ep14.html` — 통과
42. `double_slit_interference_hs2_Physics1_Ep13.html` — 통과
43. `earth_formation_gs_hs3_EarthSystem_Ep01.html` — 통과
44. `earthquake_gs_hs3_EarthSystem_Ep05.html` — 통과
45. `eclipse_earth_hs2_EarthSci1_Ep13.html` — 통과
46. `ecosystem_energy_flow_bio_hs2_Bio1_Ep06.html` — 통과
47. `ekman_transport_gs_hs3_EarthSystem_Ep06.html` — 통과
48. `elastic_energy_hs2_Physics1_Ep04.html` — 통과
49. `electric_potential_field_hs2_Physics1_Ep07.html` — 통과
50. `electrolysis_plating_cr_hs3_ChemReaction_Ep09.html` — 통과
51. `electromagnetic_induction_hs2_Physics1_Ep12.html` — 통과
52. `electron_transport_cm_hs3_CellMetab_Ep13.html` — 통과
53. `electronegativity_polarity_chem_hs2_Chem1_Ep05.html` — 통과
54. `em_wave_em_hs3_EMQuantum.html` — 통과
55. `energy_band_em_hs3_EMQuantum_Ep07.html` — 통과
56. `energy_incline_hs2_Physics1_Ep04.html` — 통과
57. `enso_earth_hs2_EarthSci1_Ep05.html` — 통과
58. `entropy_me_hs3_MatterEnergy_Ep10.html` — 통과
59. `enzyme_kinetics_cm_hs3_CellMetab_Ep08-09.html` — 통과
60. `epigenetics_gn_hs3_Genetics_Ep11.html` — 통과
61. `equilibrium_constant_chem_hs2_Chem1_Ep09-10.html` — 통과
62. `equilibrium_shift_chem_hs2_Chem1_Ep11.html` — 통과
63. `escape_velocity_dyn_hs3_MechEnergy_Ep05.html` — 통과
64. `exercise_organ_systems_bio_hs2_Bio1_Ep04.html` — 통과
65. `exoplanet_detection_pu_hs3_PlanetUniverse_Ep05.html` — 통과
66. `expression_profile_gn_hs3_Genetics_Ep15.html` — 통과
67. `force_vector_dyn_hs3_MechEnergy_Ep01.html` — 통과
68. `fuel_cell_cr_hs3_ChemReaction_Ep10.html` — 통과
69. `functional_group_cr_hs3_ChemReaction_Ep11.html` — 통과
70. `galaxy_classification_earth_hs2_EarthSci1_Ep16.html` — 통과
71. `galvanic_cell_cr_hs3_ChemReaction_Ep08.html` — 통과
72. `gas_thermo_dyn_hs3_MechEnergy_Ep08-09.html` — 통과
73. `gel_electrophoresis_gn_hs3_Genetics_Ep13.html` — 통과
74. `gene_editing_gn_hs3_Genetics_Ep14.html` — 통과
75. `gene_linkage_gn_hs3_Genetics.html` — 통과
76. `gene_regulation_gn_hs3_Genetics_Ep10.html` — 통과
77. `genomics_gn_hs3_Genetics_Ep15.html` — 통과
78. `geologic_time_fossil_earth_hs2_EarthSci1_Ep09.html` — 통과
79. `geopark_korea_earth_hs2_EarthSci1_Ep12.html` — 통과
80. `gibbs_energy_me_hs3_MatterEnergy_Ep10.html` — 통과
81. `global_circulation_gs_hs3_EarthSystem_Ep15.html` — 통과
82. `gravity_time_dyn_hs3_MechEnergy_Ep06.html` — 통과
83. `habitable_zone_pu_hs3_PlanetUniverse_Ep05.html` — 통과
84. `hall_effect_em_hs3_EMQuantum_Ep04.html` — 통과
85. `hardy_weinberg_gn_hs3_Genetics.html` — 통과
86. `heat_engine_dyn_hs3_MechEnergy_Ep10.html` — 통과
87. `heat_transfer_dyn_hs3_MechEnergy_Ep07.html` — 통과
88. `hess_law_me_hs3_MatterEnergy_Ep09.html` — 통과
89. `hubble_law_earth_hs2_EarthSci1_Ep17.html` — 통과
90. `human_pedigree_gn_hs3_Genetics_Ep02.html` — 통과
91. `ice_core_gs_hs3_EarthSci1_Ep09.html` — 통과
92. `ideal_gas_law_me_hs3_MatterEnergy_Ep01.html` — 통과
93. `immune_vaccine_bio_hs2_Bio1_Ep12_Ep14.html` — 통과
94. `impulse_safety_dyn_hs3_IntegSci1_Systems_Ep02.html` — 통과
95. `index.html` — 통과
96. `intermolecular_force_me_hs3_MatterEnergy_Ep03.html` — 통과
97. `k_temperature_cr_hs3_Chem1_Ep11.html` — 통과
98. `karyotype_bio_hs2_Bio1_Ep15.html` — 통과
99. `kinetic_theory_me_hs3_MatterEnergy_Ep01.html` — 통과
100. `laser_energy_level_em_hs3_EMQuantum_Ep12.html` — 통과
101. `latent_heat_me_hs3_MechEnergy_Ep08.html` — 통과
102. `lattice_energy_me_hs3_MatterEnergy_Ep04.html` — 통과
103. `light_dark_reaction_cm_hs3_CellMetab_Ep16.html` — 통과
104. `liquid_property_me_hs3_MatterEnergy_Ep05.html` — 통과
105. `lorentz_motion_em_hs3_EMQuantum_Ep04.html` — 통과
106. `magma_igneous_rock_earth_hs2_EarthSci1_Ep10-11.html` — 통과
107. `magnetic_materials_hs2_Physics1_Ep10.html` — 통과
108. `mass_extinction_gs_hs3_IntegSci2_Change_Ep02.html` — 통과
109. `matter_wave_em_hs3_EMQuantum_Ep13.html` — 통과
110. `mechanical_to_heat_hs2_Physics1_Ep05.html` — 통과
111. `meiosis_gamete_diversity_bio_hs2_Bio1_Ep16.html` — 통과
112. `membrane_transport_cm_hs3_CellMetab_Ep05.html` — 통과
113. `mendel_cross_gn_hs3_Genetics_Ep01.html` — 통과
114. `metal_reactivity_cr_hs3_ChemReaction_Ep08.html` — 통과
115. `midlatitude_cyclone_earth_hs2_EarthSci1_Ep03.html` — 통과
116. `milkyway_structure_pu_hs3_PlanetUniverse_Ep11.html` — 통과
117. `molar_solution_chem_hs2_Chem1_Ep13.html` — 통과
118. `mole_quantity_chem_hs2_Chem1_Ep02.html` — 통과
119. `molecular_shape_chem_hs2_Chem1_Ep06-07.html` — 통과
120. `momentum_collision_hs2_Physics1_Ep03.html` — 통과
121. `mtdna_lineage_gn_hs3_Genetics_Ep01.html` — 통과
122. `natural_selection_bio_hs2_Bio1_Ep17.html` — 통과
123. `nerve_conduction_bio_hs2_Bio1_Ep08.html` — 통과
124. `neutralization_heat_chem_hs2_Chem1_Ep14.html` — 통과
125. `newton_second_law_hs2_Physics1_Ep02.html` — 통과
126. `nuclear_energy_em_hs3_EMQuantum_Ep17.html` — 통과
127. `ocean_acid_gs_hs3_EarthSystem_Ep02.html` — 통과
128. `ocean_wave_gs_hs3_EarthSystem_Ep07.html` — 통과
129. `pcr_amplification_gn_hs3_Genetics_Ep13.html` — 통과
130. `phase_diagram_me_hs3_MatterEnergy_Ep03.html` — 통과
131. `photo_pigment_cm_hs3_CellMetab_Ep15.html` — 통과
132. `photoelectric_effect_hs2_Physics1_Ep15.html` — 통과
133. `photon_duality_em_hs3_EMQuantum_Ep13.html` — 통과
134. `photosynthesis_rate_cm_hs3_CellMetab_Ep16.html` — 통과
135. `phylogenetic_tree_bio_hs2_Bio1_Ep19.html` — 통과
136. `planet_atmosphere_pu_hs3_PlanetUniverse_Ep05.html` — 통과
137. `planet_retrograde_earth_hs2_EarthSci1_Ep13.html` — 통과
138. `plasmolysis_cm_hs3_CellMetab_Ep05.html` — 통과
139. `pn_diode_hs2_Physics1_Ep17.html` — 통과
140. `polymer_cr_hs3_ChemReaction_Ep13.html` — 통과
141. `precipitation_gs_hs3_EarthSystem_Ep12.html` — 통과
142. `projectile_motion_dyn_hs3_MechEnergy_Ep02.html` — 통과
143. `protein_secretion_cm_hs3_CellMetab_Ep03.html` — 통과
144. `quadrat_community_bio_hs2_Bio1_Ep07.html` — 통과
145. `radiometric_age_earth_hs2_EarthSci1_Ep08.html` — 통과
146. `reaction_enthalpy_me_hs3_MatterEnergy_Ep08.html` — 통과
147. `reaction_order_cr_hs3_MatterEnergy_Ep11-12.html` — 통과
148. `reaction_rate_cr_hs3_MatterEnergy_Ep13-14.html` — 통과
149. `reaction_stoichiometry_chem_hs2_Chem1_Ep03.html` — 통과
150. `recombinant_dna_gn_hs3_Genetics_Ep13.html` — 통과
151. `redox_number_cr_hs3_ChemReaction_Ep06.html` — 통과
152. `redox_titration_cr_hs3_ChemReaction_Ep06.html` — 통과
153. `resistor_power_hs2_Physics1_Ep08.html` — 통과
154. `rotation_angular_dyn_hs3_MechEnergy.html` — 통과
155. `satellite_orbit_dyn_hs3_MechEnergy_Ep04.html` — 통과
156. `seafloor_spreading_gs_hs3_EarthSystem_Ep03.html` — 통과
157. `seawater_density_earth_hs2_EarthSci1_Ep01.html` — 통과
158. `seismic_interior_gs_hs3_EarthSystem_Ep05.html` — 통과
159. `simple_harmonic_dyn_hs3_MechEnergy_Ep12.html` — 통과
160. `small_bodies_pu_hs3_PlanetUniverse_Ep04.html` — 통과
161. `solar_cell_em_hs3_EMQuantum_Ep11.html` — 통과
162. `solar_observation_pu_hs3_PlanetUniverse_Ep06.html` — 통과
163. `solar_planets_ps_hs3_PlanetUniverse_Ep03.html` — 통과
164. `solubility_henry_me_hs3_MatterEnergy_Ep06.html` — 통과
165. `solubility_ksp_cr_hs3_ChemReaction.html` — 통과
166. `solution_concentration_me_hs3_MatterEnergy_Ep07.html` — 통과
167. `sound_interference_dyn_hs3_MechEnergy_Ep15.html` — 통과
168. `space_transfer_pu_hs3_PlanetUniverse_Ep03.html` — 통과
169. `special_relativity_hs2_Physics1_Ep18.html` — 통과
170. `spectral_type_pu_hs3_EarthSci1_Ep14.html` — 통과
171. `standing_wave_dyn_hs3_MechEnergy_Ep16.html` — 통과
172. `star_cluster_pu_hs3_PlanetUniverse_Ep11.html` — 통과
173. `star_formation_pu_hs3_PlanetUniverse_Ep12.html` — 통과
174. `stellar_evolution_earth_hs2_EarthSci1_Ep15.html` — 통과
175. `superconductor_em_hs3_IntegSci1_Matter_Ep08.html` — 통과
176. `surfactant_me_hs3_MatterEnergy.html` — 통과
177. `synapse_drug_bio_hs2_Bio1_Ep09.html` — 통과
178. `telescope_pu_hs3_PlanetUniverse.html` — 통과
179. `thermohaline_earth_hs2_EarthSci1_Ep02.html` — 통과
180. `tide_gs_hs3_EarthSystem_Ep09.html` — 통과
181. `titration_buffer_cr_hs3_ChemReaction_Ep03_Ep05.html` — 통과
182. `torque_equilibrium_hs2_Physics1_Ep01.html` — 통과
183. `transcription_translation_gn_hs3_Genetics_Ep08-09.html` — 통과
184. `transformer_em_hs3_EMQuantum_Ep05.html` — 통과
185. `transpiration_cm_hs3_CellMetab.html` — 통과
186. `tunneling_em_hs3_EMQuantum_Ep15.html` — 통과
187. `typhoon_wind_earth_hs2_EarthSci1_Ep04.html` — 통과
188. `uncertainty_em_hs3_EMQuantum_Ep16.html` — 통과
189. `volcano_hazard_gs_hs3_EarthSystem_Ep04.html` — 통과
190. `water_cycle_gs_hs3_EarthSystem_Ep02.html` — 통과
191. `water_electrolysis_chem_hs2_Chem1_Ep04.html` — 통과
192. `water_ionization_ph_chem_hs2_Chem1_Ep12.html` — 통과
193. `wave_boundary_dyn_hs3_MechEnergy_Ep13.html` — 통과
194. `weak_acid_ka_cr_hs3_ChemReaction_Ep02.html` — 통과
195. `yeast_fermentation_cm_hs3_CellMetab_Ep14.html` — 통과
