# fesicsManager.github.io

fesicsExternal의 로컬 JS·CSS는 HTML에서 파일 내용의 SHA-256 앞 12자리를 `?v=`로 참조합니다. 자산 내용을 바꾸면 버전도 바뀌어 브라우저가 새 URL로 요청합니다. 외부 CDN URL과 인라인 스크립트·스타일은 유지합니다.

JS·CSS를 수정한 뒤 Node 24 이상에서 `node scripts/version-assets.ts .`를 실행하고 변경된 HTML도 함께 커밋하세요. `node scripts/version-assets.ts . --check`로 누락을 확인하고, `node --test tests/assetVersions.test.ts`로 버전 갱신·멱등성·누락 파일 처리를 검증합니다.

## 저작권

이 저장소의 실험 코드·그림·웹툰·문항 등 모든 내용은 Misodle Software(페직스)의 저작물입니다. GitHub Pages로 서비스하기 위해 공개되어 있을 뿐, 복제·수정·배포나 이를 바탕으로 한 비슷한 콘텐츠 제작(인공지능 이용 포함)은 허락하지 않습니다. 자세한 내용은 [LICENSE](LICENSE)를 보세요.

## 실험 수식 표시

`fesicsExternal/math-typography.js`는 일반 HTML과 동적 결과의 명시적인 아래첨자(`E_g`), 지수(`a^(1/n)`), 제곱근·n제곱근을 표시합니다. HTML 루트는 MathML로, Canvas 루트는 피제곱근의 너비에 맞춰 그립니다. Canvas의 첫 그리기 전에 적용되도록 해당 스크립트는 `head`에서 불러옵니다. 기존 TeX/MathJax/KaTeX와 코드·입력 필드는 보존합니다. 표기 보정을 제외할 영역에는 `data-math-typography="off"`를 지정할 수 있습니다.

피제곱근이나 지수가 여러 항이면 `√(a² + b²)`, `x^(m+n)`처럼 범위를 괄호로 명시하세요. 계수나 변수 이름만 보고 수식의 의미를 추측하지 않습니다.

회귀 검사는 설치된 Chrome과 Playwright로 `node --test tests/math-typography.test.cjs`를 실행합니다. Playwright가 공용 위치에 설치되어 있으면 `PLAYWRIGHT_MODULE` 환경 변수에 해당 모듈 경로를 지정하세요.
