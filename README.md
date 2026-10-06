# fesicsManager.github.io

fesicsExternal의 로컬 JS·CSS는 HTML에서 파일 내용의 SHA-256 앞 12자리를 `?v=`로 참조합니다. 자산 내용을 바꾸면 버전도 바뀌어 브라우저가 새 URL로 요청합니다. 외부 CDN URL과 인라인 스크립트·스타일은 유지합니다.

JS·CSS를 수정한 뒤 Node 24 이상에서 `node scripts/version-assets.ts .`를 실행하고 변경된 HTML도 함께 커밋하세요. `node scripts/version-assets.ts . --check`로 누락을 확인하고, `node --test tests/assetVersions.test.ts`로 버전 갱신·멱등성·누락 파일 처리를 검증합니다.

## 저작권

이 저장소의 실험 코드·그림·웹툰·문항 등 모든 내용은 Misodle Software(페직스)의 저작물입니다. GitHub Pages로 서비스하기 위해 공개되어 있을 뿐, 복제·수정·배포나 이를 바탕으로 한 비슷한 콘텐츠 제작(인공지능 이용 포함)은 허락하지 않습니다. 자세한 내용은 [LICENSE](LICENSE)를 보세요.
