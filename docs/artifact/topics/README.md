# 아티팩트 폴더 규칙

```text
docs/artifact/
├── index.html                 ← 유일한 공개 목차 (catalog.json에서 생성)
├── catalog.json               ← 주제 → 분야 → 문서 순서
├── flow-*.html 등             ← 기존 공개 URL, 이동하지 않음
├── images/                    ← 기존 문서의 공유 이미지
├── styles/                    ← 기존 문서의 분리된 CSS
└── topics/
    └── <subject>/
        └── <topic>/
            └── <slug>/
                ├── index.html ← 새 아티팩트의 고정 URL
                └── images/    ← 이 문서만 쓰는 이미지가 필요할 때
```

`subject`는 TRACEBACK 같은 프로젝트 또는 데이터베이스 시스템 같은 학습
영역입니다. `topic`은 그 안의 분야, `slug`는 개별 아티팩트입니다. 새 분야가
생겨도 목차 HTML을 손으로 고치지 않고 `catalog.json`에 항목만 추가합니다.

기존 `docs/artifact/*.html`과 `images/*`는 공개 URL을 유지하기 위해 이동하지 않습니다.
새 주제는 `topics/<subject>/<topic>/<slug>/index.html`로 추가하고, 그 문서만
쓰는 이미지는 같은 디렉터리의 `images/`에 둡니다. 하나의 HTML로 완결되는
시각 문서는 그 폴더의 `index.html`에 CSS·동작을 포함하고
`<meta name="artifact-format" content="standalone">`으로 표시합니다. 다른
문서는 `styles/`의 CSS를 연결합니다. 의견 버튼을
사용할 때는 문서의 위치에서 `docs/artifact/feedback.js`까지 올바른 상대
경로를 지정하고 `scripts/verify_site.py`로 확인합니다.

새 문서를 목차에 넣을 때는 `docs/artifact/catalog.json`의 해당 subject/topic에
항목을 추가하고 `python3 scripts/build_index.py`를 실행합니다. 기존 항목의
URL을 옮겨야 한다면 이전 URL을 남겨 두고 안내 또는 redirect를 제공해
의견 파일의 `document_url`과 절 링크가 끊기지 않게 합니다.

현재 주제는 TRACEBACK의 인프라·인증, 아티팩트 운영입니다. 다른 프로젝트나
강의 학습 자료도 새 subject/topic으로 추가할 수 있습니다.
