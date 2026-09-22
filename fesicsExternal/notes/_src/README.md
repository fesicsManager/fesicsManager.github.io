# 자습 노트 생성 도구

- content/<폴더>/<실험이름>.json : 노트 내용 (여기를 고치면 노트가 바뀜)
- build_note.js  : json → 노트 HTML
- apply_batch.js : 폴더 단위 일괄 적용 (노트 생성 + 실험 파일에 탭 링크 주입 + index.html 링크)
- extract_sources.js : 실험 HTML에서 원리·문제 텍스트 추출 (노트 작성용 원자료)

## 다시 적용하기 (내용을 고친 뒤)
    node apply_batch.js "<fesicsExternal 경로>" "<백업 폴더 경로>" milddle3Phy milddle3PhyAdv

여러 번 실행해도 안전 (마커 블록을 찾아 교체). 백업은 최초 1회만 만들어짐.
