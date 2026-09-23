# 고3 확률과 통계 HTML 26개 검토 보고서

- 검토일: 2026-09-23
- 대상: Google Drive `high3ProbStat` 폴더의 `hz_093`~`hz_118` HTML 26개 (`index.html` 제외)
- 방법: 파일별 화면 문구, 입력값, JavaScript 계산식 정적 대조. 브라우저 상호작용·모바일 표시·외부 링크의 실제 실행은 확인하지 않음.
- 집계: 수정 11개, 보완 6개, 정적 검토 양호 9개. ‘양호’는 모든 입력과 실행 환경의 무결성을 보증하지 않음.

## 파일별 결과

| 번호 | 판정 | 근거와 조치 |
|---|---|---|
| [093](https://drive.google.com/file/d/1ImZhMoi5jC8jOoK6RMgmUKOWyGeh3eAh/view?usp=drivesdk) | 보완 | 목걸이를 다시 2로 나누는 설명은 서로 다른 물건 3개 이상일 때로 한정. |
| [094](https://drive.google.com/file/d/12VJ7f3cCJWpnmARQZY8H_s_IKJqiLQ3R/view?usp=drivesdk) | 양호 | 함수 n^m, 일대일함수 nP m 계산 일치. |
| [095](https://drive.google.com/file/d/1Ed_WvcXCu1oqswXVkc_jbtCmR4O261Ho/view?usp=drivesdk) | 양호 | 격자 누적합과 조합 공식 일치. |
| [096](https://drive.google.com/file/d/1opV9TO-9PcQm7EZzIbI09s_-_9gmpYn7/view?usp=drivesdk) | 보완 | 제목은 세 질문인데 입력과 공식 분기는 순서·중복 두 질문만 처리. 구별 여부를 추가하거나 제목 변경. |
| [097](https://drive.google.com/file/d/1p7zIf4a85qsIysZEfexMZmCJ7WwDaRY4/view?usp=drivesdk) | 수정 | 입력은 ‘양 끝에 올 후보 수 k’, 계산과 결과는 ‘맨 앞 후보 k명’만 처리. 양 끝 조건으로 오해됨. 입력 문구를 맨 앞 조건으로 고치거나 양 끝을 모두 계산. |
| [098](https://drive.google.com/file/d/1Ht6KVjwlJj1fTa77zaEqoWrWcIvZuUig/view?usp=drivesdk) | 양호 | 음이 아닌 해와 양의 정수해를 열거하여 조합과 대조. |
| [099](https://drive.google.com/file/d/1k20NwU4mkQJFY5O14AAE06-S5AsX7NtA/view?usp=drivesdk) | 양호 | 이항계수와 항 개수 계산 일치. |
| [100](https://drive.google.com/file/d/1tVf9TFyCK9NPbaH1Sc6iRSIaS8iF64W-/view?usp=drivesdk) | 수정 | ‘r번째 항의 계수’ 비교값을 C(n,r+1)2^(r+1)로 계산해 r=0일 때 두 번째 항을 보여 줌. r번째와 (r+1)번째를 비교하려면 r≥1에서 C(n,r-1)2^(r-1) 사용; r=0은 해당 항 없음. |
| [101](https://drive.google.com/file/d/1YQodFWrDSDR_B1kmsRhhI5LrShJRWO-8/view?usp=drivesdk) | 양호 | 계수합 2^n과 교대합 0 계산 일치. |
| [102](https://drive.google.com/file/d/1cwzvDeb_HEAH8BV_rNsZHN1niXe7MgP6/view?usp=drivesdk) | 양호 | 두 동전의 순서 있는 네 결과와 무순서 세 결과의 비등확률 설명 적절. |
| [103](https://drive.google.com/file/d/1-qljCPRapwquDuEJ5tdcZ45Jlg39KF4m/view?usp=drivesdk) | 수정 | ‘유한 표본공간에서는 P(A)=0 iff A=공집합’은 모든 근원사건의 확률이 양수일 때만 성립. 확률 0인 원소를 허용하면 반례 있음. 또한 Math.random()은 정확히 0.5가 나올 수 있는 유한 격자 난수라 연속분포 실험으로 엄밀하지 않음. |
| [104](https://drive.google.com/file/d/1zgNDTBF-JbXlHAoJPR4lTdRGcjeHiI7O/view?usp=drivesdk) | 양호 | 비복원·복원 두 번 빨간 공 확률 공식 일치. |
| [105](https://drive.google.com/file/d/1QWaky-8sbOwH_TSCjcN8WQFEIYIswyyX/view?usp=drivesdk) | 보완 | 연속 k회 직후의 관찰 표본 수가 작거나 0이면 비율을 0으로 표시. 표본 부족을 별도 표시하고 k·n에 따라 관찰 횟수 안내. |
| [106](https://drive.google.com/file/d/1C6A6qL_1-Fdo-1DB49tchWHOQyBS_Fng/view?usp=drivesdk) | 양호 | 여사건과 이항전개 직접 합의 결과 일치. ‘적어도은’ 오탈자 수정. |
| [107](https://drive.google.com/file/d/18RHiVZCVhqaeWGbrbpGirOdubxD-dx5G/view?usp=drivesdk) | 양호 | 두 순서의 결합확률 rb/[n(n−1)] 일치. |
| [108](https://drive.google.com/file/d/1LXEWSs33yFbCjPUFE7-7GhydUzISGvtJ/view?usp=drivesdk) | 수정 | 독립 판정을 |P(B|A)−P(B)|<0.005로 근사 처리하므로 실제 종속도 독립으로 판정 가능. 정수 교차곱 a·d=b·c로 정확히 판정하고 분모 0 입력 처리. |
| [109](https://drive.google.com/file/d/1tamOCQt04e38OfNZtkBfd6C1YcLLEb_M/view?usp=drivesdk) | 수정 | 질병 검사 민감도와 특이도를 하나의 ‘정확도’ s로 묶고 인원을 각각 반올림함. p=10, s=99%일 때 10명 전원 양성, 건강자 100명 위양성으로 나와 ‘약 9%’ 설명은 모형상 근사임. 두 비율을 구분하고 기대 인원 소수 또는 반올림 표기를 명시. |
| [110](https://drive.google.com/file/d/17JX0ZwlMg9Ph6njwVEzBdytgh_AnAs7a/view?usp=drivesdk) | 수정 | a+b=0 또는 a+c=0일 때 조건부확률 분모가 0. 입력 하한 확인 후, 허용한다면 ‘정의되지 않음’ 처리. |
| [111](https://drive.google.com/file/d/14iVpUo7MjkzhF_F07kbl94oS0v2Q0nhD/view?usp=drivesdk) | 수정 | 수학 원리에서 ‘확률변수의 정의역이 사건들의 모임’은 잘못. 정의역은 표본공간의 근원결과 ω, X:Ω→R로 고침. |
| [112](https://drive.google.com/file/d/1LXkociveog12DZs805HnDobg23olq5zW/view?usp=drivesdk) | 보완 | ‘합<1이면 빠진 경우, >1이면 겹쳐 센 것’은 가능한 해석일 뿐. 임의 입력값에서는 단순 오류일 수도 있으므로 단정 완화. |
| [113](https://drive.google.com/file/d/195Z4Z1agm1vqqsiUTMhGZhDf0m_AQz-q/view?usp=drivesdk) | 보완 | 확률 가중치를 입력 합으로 정규화하므로 입력 숫자가 그대로 확률이라는 인상을 막고 ‘가중치’로 표시. |
| [114](https://drive.google.com/file/d/1zGlHLNDkB9oY7edz1PC9i-IEzOlA7VAl/view?usp=drivesdk) | 수정 | a가 음수여도 ‘분산은 줄지 않는다’는 문장은 오류. |a|<1이면 분산이 감소하고 a<0도 가능. 입력 범위와 설명을 맞춤. |
| [115](https://drive.google.com/file/d/1uxujTWkWpuRMpjnvID8UUbMozpUH16WZ/view?usp=drivesdk) | 수정 | 표본이 크면 편향 추출도 ‘빗나간 곳에 수렴’한다는 설명을 쓰지만, 실제 코드는 상위 600개에서 복원추출하며 표본 크기만 바꿀 때 새 표본을 뽑음. 한 번의 무작위 표본이 모평균 근처에 반드시 모인다는 문구도 과장. 기대값·반복분포와 개별 오차를 구분. |
| [116](https://drive.google.com/file/d/1TeAKO59mbM5AO-BD1XTzlO5cDEG90pq6/view?usp=drivesdk) | 수정 | ‘모집단이 어떤 모양이든’과 ‘n≥30이면 충분’은 무한분산·심한 왜도 등의 조건 없이 성립하지 않음. 독립동일분포와 유한분산 가정 및 n=30의 비보편성 명시. |
| [117](https://drive.google.com/file/d/1VXKfzGSARrxb8axFNP7ZnUOqNEhmfKre/view?usp=drivesdk) | 보완 | σ를 아는 정규모집단 또는 정규근사가 가능한 조건의 z 구간 길이임을 표기. ‘정밀도 두 배면 비용 네 배’는 비용이 표본 수에 비례한다는 가정 붙이기. |
| [118](https://drive.google.com/file/d/17O0KpAVf6_BAAXlEP95nDQxtgkj4HAqt/view?usp=drivesdk) | 수정 | 모표준편차 미지인데 데이터의 n분모 표준편차를 1.96·sd/√n에 대입해 ‘95% 신뢰구간’ 표시. 표본표준편차(n−1 분모)와 t 임계값 사용하거나 모표준편차를 아는 모형으로 명시. |

## 우선 수정 및 재현 예

1. **097 조건 입력 불일치:** `k=2, n=5`에서 코드 결과는 `2×4!=48`로 맨 앞 자리만 제한합니다. ‘양 끝에 올 후보’라는 입력 이름과 다릅니다.
2. **108 독립 판정:** 코드가 `abs(P(B|A)-P(B))<0.005`로 판단합니다. 정수 네 칸에서는 `a*d===b*c`가 정확한 조건입니다.
3. **109 검사 표:** `p=10, s=99`에서 양성 환자 10, 위양성 100, 총 110명으로 약 9.09%가 나오지만 각각 반올림한 인원입니다. 정확도는 민감도·특이도 두 값이 필요한 개념입니다.
4. **111 정의역:** 확률변수는 표본공간 Ω에서 실수로 가는 함수입니다. 사건들의 모임을 정의역으로 적은 문장을 교정합니다.
5. **118 구간 추정:** 모표준편차를 모르는 표본에서 `sd=√(Σ(x−x̄)²/n)`과 1.96을 그대로 써 95% 구간이라 표시합니다. 추정 방식의 전제를 명확히 하고 계산식을 일치시킵니다.

## 범위 확인

요청한 ZIP과 정확히 같은 이름의 단일 압축파일은 검색 결과에서 확인되지 않았습니다. 동일한 `high3ProbStat` 폴더에 있는 26개 HTML을 검토했습니다. 원본 HTML은 수정하지 않았으며, 이 보고서가 수정 지침입니다.
