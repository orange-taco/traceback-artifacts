# 새 아티팩트 위치

기존 `docs/artifact/*.html`과 `images/*`는 공개 URL을 유지하기 위해 이동하지 않습니다.
새 주제는 `topics/<subject>/<topic>/<slug>/index.html`로 추가하고, 그 문서만
쓰는 이미지는 같은 디렉터리의 `images/`에 둡니다. 하나의 HTML로 완결되는
시각 문서는 그 폴더의 `index.html`에 CSS·동작을 포함합니다.

새 문서를 목차에 넣을 때는 `docs/artifact/catalog.json`의 해당 subject/topic에
항목을 추가하고 `python3 scripts/build_index.py`를 실행합니다. 기존 항목의
URL을 옮겨야 한다면 이전 URL을 남겨 두고 안내 또는 redirect를 제공해
의견 파일의 `document_url`과 절 링크가 끊기지 않게 합니다.

현재 주제는 TRACEBACK의 인프라·인증, 아티팩트 운영입니다. 다른 프로젝트나
강의 학습 자료도 새 subject/topic으로 추가할 수 있습니다.
