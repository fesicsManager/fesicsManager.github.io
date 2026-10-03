# fesicsManager.github.io

fesicsExternal의 로컬 JS·CSS는 HTML에서 파일 내용의 SHA-256 앞 12자리를 `?v=`로 참조합니다. 자산 내용을 바꾸면 버전도 바뀌어 브라우저가 새 URL로 요청합니다. 외부 CDN URL과 인라인 스크립트·스타일은 유지합니다.

JS·CSS를 수정한 뒤 Node 24 이상에서 `node scripts/version-assets.ts .`를 실행하고 변경된 HTML도 함께 커밋하세요. `node scripts/version-assets.ts . --check`로 누락을 확인하고, `node --test tests/assetVersions.test.ts`로 버전 갱신·멱등성·누락 파일 처리를 검증합니다.
