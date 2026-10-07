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
Codex Cloud로 수정할 때는 게시된 개인 환경 `TRACEBACK Study (3 repos)`를
선택합니다. 현재 이 환경에는 문서 저장소, 백엔드 저장소, 프런트 저장소가
GitHub 저장소로 연결되어 있습니다. 비공개 의견 저장소를 만들었다면
그 저장소도 환경에 추가하고 재게시해야 Codex Cloud에서 의견 파일을 읽을 수
있습니다. 연결되지 않은 저장소를 Codex가 자동으로 볼 수 있다고 가정하지
않습니다.

GitHub Pages는 계속 공개 읽기 사이트입니다. 의견 UI와 저장 서버의 코드는
이 저장소에 준비되어 있지만, 별도 GitHub App·Cloudflare Worker·비공개
저장소를 설정하고 Pages를 다시 게시하기 전에는 의견 버튼이 나타나지
않습니다. iPad에서 의견을 저장해도 Codex 작업이나 문서 수정은 시작되지
않습니다. 수정할 때는 본인이 Codex Cloud에서 별도 작업을 시작하고 문서
PR을 검토합니다.

## iPad 의견 저장

구성 및 배포 절차는 [`feedback-worker/README.md`](feedback-worker/README.md)에
있습니다. 공개 문서에서 **의견 남기기**를 누르면 작성 화면으로 이동합니다.
문구 선택은 필요하지 않습니다. 위치를 자유롭게 적고, 문서 전체의 맥락에
대한 의견도 남길 수 있습니다. 저장되는 JSON에는 문서 URL, 절 ID(있으면),
선택 문구(null), 위치 설명, 의견, 게시 revision, 작성 시각과 GitHub 작성자
ID가 포함됩니다. 이 파일은 `oscar2272/traceback-feedback` 비공개 저장소에만
기록됩니다.

서버는 GitHub 로그인에서 확인한 계정 ID가 `oscar2272`의 ID인지 검사하고,
로그인 세션과 CSRF 토큰을 다시 확인한 뒤 저장합니다. 브라우저에 GitHub
토큰이나 OpenAI API 키를 넣지 않습니다. 의견 저장용 API는 Codex 작업이나
artifact 수정 API를 제공하지 않습니다.

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
   두 코드 저장소의 기본 브랜치는 `main`이므로, 개발 중인 내용은
   `development` 또는 대상 PR 브랜치를 명시해 확인합니다.
2. 문서 작성 스킬에 따라 HTML·이미지와 링크를 수정합니다.
3. `python3 scripts/verify_site.py`로 상대 링크를 확인합니다.
4. 문서 저장소의 PR에서 변경을 검토한 뒤 `main`으로 병합해 게시합니다.

GitHub Pages는 공개 사이트입니다. 문서에 넣을 AWS·GitHub 화면에는
비밀값이나 개인 정보가 보이지 않는지 게시 전에 확인합니다.
