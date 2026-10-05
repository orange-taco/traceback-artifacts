# TRACEBACK Artifacts

TRACEBACK의 학습용 시각 문서를 백엔드 코드와 독립적으로 관리합니다.

- 문서 시작: [`docs/artifact/index.html`](docs/artifact/index.html)
- iPad 읽기 주소: [TRACEBACK 학습 목차](https://orange-taco.github.io/traceback-artifacts/)
- 문서 작성 기준: [`.codex/skills/auth-flow-visualizer/SKILL.md`](.codex/skills/auth-flow-visualizer/SKILL.md)
- 설명의 근거가 되는 백엔드 코드: [`orange-taco/traceback`](https://github.com/orange-taco/traceback)
- 프런트·Vercel 코드: [`orange-taco/traceback-client`](https://github.com/orange-taco/traceback-client)

## 어디서 무엇을 수정하나요?

이 저장소가 HTML·이미지·작성 스킬의 원본입니다. 백엔드 저장소의 코드를
설명할 때는 먼저 백엔드 또는 프런트 코드와 배포 설정을 확인하고, 문서의
소스 링크에 확인한 Git revision을 남깁니다. 이 저장소는 앱 코드를 복사해서
보관하지 않습니다.

iPad에서 문서를 읽는 데 로컬 clone이나 `git pull`은 필요하지 않습니다.
Codex Cloud로 수정할 때는 이 문서 저장소, 백엔드 저장소, 프런트 저장소를
같은 Cloud 환경의 GitHub 저장소로 등록합니다. Codex가 세 저장소를 읽고,
문서 변경은 이 저장소에만 제출합니다. 연결되지 않은 저장소를
Codex가 자동으로 볼 수 있다고 가정하지 않습니다.

현재 GitHub Pages는 읽기 전용 정적 사이트입니다. 페이지에서 Codex에 직접
수정을 요청하거나 댓글을 저장하는 기능은 아직 없습니다. iPad에서는
사이트에서 대상 문서의 제목·절·수정 내용을 확인한 뒤, Codex Cloud에서
이 환경을 선택해 요청하고 문서 PR을 검토합니다.

## 로컬 확인

저장소 루트에서 다음 명령으로 사이트 내부의 파일·fragment 링크를 검사합니다.

```sh
python3 scripts/verify_site.py
```

HTML은 브라우저에서 `docs/artifact/index.html`로 열 수 있습니다. `main`
업데이트는 GitHub Pages 워크플로가 게시합니다.

## 수정 흐름

1. 설명 대상에 따라 `orange-taco/traceback`과
   `orange-taco/traceback-client`의 대상 브랜치와 파일을 확인합니다.
   Cloud 환경에 세 저장소를 연결하면 iPad에 clone을 둘 필요가 없습니다.
2. 문서 작성 스킬에 따라 HTML·이미지와 링크를 수정합니다.
3. `python3 scripts/verify_site.py`로 상대 링크를 확인합니다.
4. 문서 저장소의 PR에서 변경을 검토한 뒤 `main`으로 병합해 게시합니다.

GitHub Pages는 공개 사이트입니다. 문서에 넣을 AWS·GitHub 화면에는
비밀값이나 개인 정보가 보이지 않는지 게시 전에 확인합니다.
