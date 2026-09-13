# 외부 실험 iframe 자동 높이 검증 기록

실행 명령:

```text
cd ../fesics-react-web
corepack yarn playwright test --config=../fesicsManager.github.io/playwright.config.mjs
```

검증 결과: 4개 통과.

- 모바일 세로 `milddle1BioGeo/01_stimulus_response_lab.html`: 초기 자연 높이와 body margin 포함 높이 일치, 동적 콘텐츠 추가·제거 시 grow/shrink, 재요청 응답, 257자 requestId 거부 확인.
- 모바일 가로 `milddle3Bio/01_sensory_organs_lab.html`: 동일한 자연 높이 계산과 grow/shrink, 대표 레이아웃 스크린샷 생성 확인.
- standalone: handshake가 없으면 `min-height: 100vh`와 기존 레이아웃 유지 확인.
- `ResizeObserver` 미지원 환경: 초기 높이 응답, window resize 경로, `pagehide/pageshow` 복귀 후 높이 재전송 확인.

추가 정적 검사:

- `node --check fesicsExternal/embed-resize.js` 통과.
- `fesicsExternal` 아래 HTML 238개 모두 공통 스크립트 참조가 정확히 1개이고 `</body>`가 정확히 1개인지 확인.
- `git diff --check` 통과.

브라우저 테스트는 로컬 정적 서버에서 수행했으며 커밋·푸시·배포는 하지 않았다.
