"""Build the five short TRACEBACK flow pages from reviewed source references."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "docs" / "artifact"
BACKEND = "9a8794919142587789a7a7b9818ec62ec1fb75b5"
CLIENT = "afd7664ce2e1b5d58f8f259b73b352878bdbf0e8"


def source(repo: str, revision: str, path: str, lines: str, label: str) -> str:
    return (
        f'<a href="https://github.com/orange-taco/{repo}/blob/{revision}/{path}#L{lines}">'
        f"{escape(label)}</a>"
    )


PAGES = [
    {
        "file": "flow-1-system.html",
        "num": "01",
        "kicker": "서비스의 전체 경계",
        "title": "TRACEBACK은 어디서 화면을 보여주고, 어디서 요청을 처리할까?",
        "lead": "TRACEBACK은 고객이 보는 프런트엔드와 Django API를 분리한 서비스입니다. 아래 그림은 고객 요청이 지나가도록 설계된 경로입니다. 실제 외부 요청 성공 여부는 단계별 상태를 따로 확인해야 합니다.",
        "nodes": [
            ("고객", "브라우저", "화면 열기·API 요청", "client"),
            ("프런트엔드", "Vercel · React Router", "페이지 제공·API 경로 rewrite", "front"),
            ("백엔드", "EC2 · Django", "인증·비즈니스 로직", "api"),
            ("데이터", "RDS · PostgreSQL", "계정·서비스 데이터", "data"),
        ],
        "caption": "브라우저의 페이지 요청은 Vercel에서 처리합니다. /api, /accounts, /_allauth 요청은 Vercel 설정의 DJANGO_ORIGIN을 통해 Django 쪽으로 전달하도록 정의되어 있습니다. Django가 DB를 사용합니다.",
        "status": "프런트와 rewrite는 개발 브랜치 코드에 정의되어 있습니다. 2026-10-04 관찰 기록에는 API HTTPS가 연결 거부 상태였습니다. 지금의 외부 접속은 별도로 다시 확인해야 합니다.",
        "links": [
            source("traceback-client", CLIENT, "vercel.ts", "1-L37", "클라이언트 development · Vercel rewrite 1–37행"),
            source("traceback", BACKEND, "config/settings/base.py", "1", "백엔드 development · Django 설정"),
            '<a href="traceback-system-guide.html">시스템·인증·CI/CD 상세 참고</a>',
            '<a href="auth-session-allauth-guide.html">인증 개념과 구현</a>',
        ],
    },
    {
        "file": "flow-2-access.html",
        "num": "02",
        "kicker": "운영자의 서버 접속",
        "title": "운영자는 개발 EC2에 어떻게 들어갈까?",
        "lead": "운영자가 터미널에서 EC2의 셸을 여는 경로입니다. TRACEBACK의 개발 환경은 Session Manager(SSM)를 사용하도록 준비했습니다.",
        "nodes": [
            ("운영자", "Mac · AWS CLI", "Identity Center 로그인", "client"),
            ("AWS", "Session Manager", "세션 권한 검사·중계", "aws"),
            ("개발 서버", "EC2 · SSM Agent", "AWS 서비스로 연결", "api"),
            ("결과", "EC2의 Linux 셸", "명령 입력·결과 확인", "data"),
        ],
        "caption": "사람은 AWS에 세션을 요청하고, EC2의 Agent는 자신의 IAM 역할과 네트워크 경로로 AWS에 연결합니다. 셸 접속을 위해 EC2의 SSH 22번 포트를 열 필요가 없습니다.",
        "status": "2026-10-04 문서 기록에는 개발 EC2의 SSM Agent Online과 인바운드 22 차단이 확인되어 있습니다. 콘솔 상태는 바뀔 수 있으므로 접속 시 다시 확인합니다.",
        "links": [
            source("traceback", BACKEND, "docs/deployment.md", "83-L105", "백엔드 development · EC2 역할과 SSM 준비"),
            '<a href="1-aws-ssm-ssh-learning-guide.html">SSH·SSM·IAM·VPC 개념과 접속 명령</a>',
        ],
    },
    {
        "file": "flow-3-deploy.html",
        "num": "03",
        "kicker": "코드가 서버에 도착하는 길",
        "title": "개발 코드는 어떻게 EC2에 배포될까?",
        "lead": "백엔드 development 브랜치에 코드가 반영되면 GitHub Actions가 검증한 뒤 하나의 컨테이너 이미지를 ECR에 저장하고 SSM으로 개발 EC2에 배포하도록 구성되어 있습니다.",
        "nodes": [
            ("소스", "GitHub development", "push 또는 PR", "client"),
            ("검증", "Actions · CI", "품질·테스트", "front"),
            ("이미지", "Amazon ECR", "SHA 이미지·digest", "aws"),
            ("서버", "SSM → 개발 EC2", "pull·migration·healthcheck", "api"),
        ],
        "caption": "검증에 성공한 push만 배포 workflow를 엽니다. EC2는 ECR 이미지를 가져와 자신의 환경변수와 DB로 실행합니다. 프런트엔드의 Vercel 배포는 별도 경로입니다.",
        "status": "workflow는 development 코드에서 확인했습니다. 실제 배포 완료 여부와 외부 HTTPS·DB 연결은 CI 설정만으로 증명되지 않습니다. 생산 환경은 승인·승격 경로를 별도로 확인해야 합니다.",
        "links": [
            source("traceback", BACKEND, ".github/workflows/ci.yml", "1-L60", "백엔드 development · CI 1–60행"),
            source("traceback", BACKEND, "docs/deployment.md", "1-L20", "백엔드 development · 배포 계약 1–20행"),
            '<a href="2-dev-server-first-deployment.html">OIDC·ECR·SSM·EC2·RDS 개념과 배포 순서</a>',
        ],
    },
    {
        "file": "flow-4-address.html",
        "num": "04",
        "kicker": "API 서버의 이름과 주소",
        "title": "Vercel은 개발 API 서버를 어떤 주소로 찾을까?",
        "lead": "개발 API는 도메인 이름을 통해 EC2의 고정 공인 IP에 연결하도록 설정했습니다. 이름을 찾는 것과 HTTPS 요청에 성공하는 것은 서로 다른 단계입니다.",
        "nodes": [
            ("프런트 설정", "DJANGO_ORIGIN", "https://api.dev-traceback.com", "front"),
            ("이름", "Route 53 · A 레코드", "api.dev-traceback.com", "aws"),
            ("주소", "Elastic IP", "3.34.78.140", "api"),
            ("대상", "개발 EC2", "Nginx → Django 예정", "data"),
        ],
        "caption": "Vercel의 rewrite가 API origin을 사용합니다. DNS는 도메인의 IP를 알려주고, Elastic IP는 개발 EC2에 붙습니다. 그 다음 HTTPS/TLS와 API 앱이 준비되어야 응답이 돌아옵니다.",
        "status": "2026-10-04 관찰 기록에는 도메인·A 레코드·EIP와 HTTP 80 경로가 확인됐고, TLS 443과 API 연결은 대기 중이었습니다. 현재 AWS·Vercel 콘솔 상태는 재확인이 필요합니다.",
        "links": [
            source("traceback-client", CLIENT, "vercel.ts", "1-L37", "클라이언트 development · origin 검증·rewrite 1–37행"),
            '<a href="3-development-ip-domain-guide.html">IP·도메인·EIP 선택과 설정 상세</a>',
        ],
    },
    {
        "file": "flow-5-dns.html",
        "num": "05",
        "kicker": "이름을 찾은 뒤 웹 연결",
        "title": "api.dev-traceback.com을 열면 어떤 순서로 연결될까?",
        "lead": "도메인 조회는 접속할 IP를 찾는 단계입니다. 그 답을 받은 다음에야 브라우저 또는 Vercel이 EC2의 HTTPS 서비스에 연결을 시도합니다.",
        "nodes": [
            ("요청자", "Vercel 또는 브라우저", "API 도메인 조회", "client"),
            ("주소 찾기", "DNS · Route 53", "A 레코드 → EIP", "aws"),
            ("암호화 연결", "EC2 · TLS 443", "인증서·Nginx 필요", "api"),
            ("응답", "Django → RDS", "API·DB 동작 확인", "data"),
        ],
        "caption": "Route 53이 웹 요청을 전달하는 것은 아닙니다. DNS가 IP를 알려준 뒤 요청자가 그 IP의 443번 포트에 새 연결을 만듭니다. 서버와 DB까지 정상이어야 API 응답이 완성됩니다.",
        "status": "2026-10-04에는 DNS 답은 확인됐지만 HTTPS 연결은 실패했습니다. DNS 성공을 서비스 배포 완료로 읽지 않습니다. 최신 상태는 TLS, Nginx, Django, RDS를 순서대로 검증해야 합니다.",
        "links": [
            source("traceback-client", CLIENT, "vercel.ts", "20-L35", "클라이언트 development · API rewrite 20–35행"),
            '<a href="4-dns-resolution-map.html">resolver·권한 DNS·TLS 개념과 상세 그림</a>',
        ],
    },
]


STYLE = """
  :root{font-family:system-ui,-apple-system,'Apple SD Gothic Neo',sans-serif;color:#173042;background:#f4f7f8;line-height:1.6}
  *{box-sizing:border-box}body{margin:0}main{max-width:1110px;margin:auto;padding:24px clamp(16px,4vw,44px) 90px}
  a{color:#075c83}a:focus-visible,button:focus-visible{outline:3px solid #e39a36;outline-offset:3px}
  .top{display:flex;justify-content:space-between;gap:12px;align-items:center}.top a{font-weight:700}.top button{border:1px solid #9bb7c6;border-radius:8px;background:white;padding:8px 12px;font:inherit;cursor:pointer}
  .hero{padding:clamp(22px,5vw,50px) 0 30px}.eyebrow{color:#096a8e;font-size:.78rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase}
  h1{font-size:clamp(2rem,5.5vw,3.8rem);line-height:1.16;letter-spacing:-.045em;max-width:17ch;margin:10px 0 18px;word-break:keep-all}
  .lead{max-width:77ch;font-size:1.08rem;color:#4b6270}h2{font-size:1.3rem;margin:0 0 8px}.panel{background:white;border:1px solid #cad9e1;border-radius:16px;padding:clamp(18px,3vw,30px);margin:15px 0}
  .flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;list-style:none;padding:0;margin:24px 0}.flow li{position:relative;min-width:0;border:2px solid #7eaebd;border-radius:12px;padding:15px;background:#edf7f9}
  .flow li:not(:last-child)::after{content:'→';position:absolute;right:-19px;top:42%;color:#096a8e;font-size:1.3rem;font-weight:900}.flow small{display:block;font-weight:800;color:#096a8e}.flow strong{display:block;margin:4px 0;font-size:1.08rem;line-height:1.25}.flow span{display:block;color:#536977;font-size:.82rem}.flow .api{border-color:#9b8ccd;background:#f5f2fc}.flow .data{border-color:#7aaa8d;background:#f0f8f2}
  .caption{margin:0;color:#405768}.status{border-left:4px solid #b47822;background:#fff8eb;padding:14px 18px;color:#5d472d}.links{display:flex;flex-wrap:wrap;gap:10px;list-style:none;margin:15px 0 0;padding:0}.links a{display:block;border:1px solid #b9d0dc;border-radius:9px;background:#f1f8fb;padding:10px 12px;text-decoration:none;font-weight:650;font-size:.9rem}.links a:hover{background:#e2f1f7}
  .next{display:flex;justify-content:space-between;gap:12px;margin-top:25px;font-weight:750}.source-note{font-size:.78rem;color:#637481;margin-top:14px}
  @media(max-width:700px){.flow{grid-template-columns:1fr;gap:21px}.flow li:not(:last-child)::after{content:'↓';left:50%;right:auto;top:auto;bottom:-25px}.next{flex-direction:column}.top{align-items:start}.top button{flex:none}}
  @media print{body{background:white}.top,button,.next{display:none!important}.panel,.flow li{break-inside:avoid}.flow{grid-template-columns:repeat(4,minmax(0,1fr))}a{color:inherit}}
"""


def render(page: dict, index: int) -> str:
    nodes = "".join(
        f'<li class="{kind}"><small>{escape(owner)}</small><strong>{escape(name)}</strong><span>{escape(role)}</span></li>'
        for owner, name, role, kind in page["nodes"]
    )
    links = "".join(f"<li>{link}</li>" for link in page["links"])
    prev_link = f'<a href="{PAGES[index-1]["file"]}">← {PAGES[index-1]["num"]} 이전 흐름</a>' if index else '<a href="index.html">← 전체 구조</a>'
    next_link = f'<a href="{PAGES[index+1]["file"]}">{PAGES[index+1]["num"]} 다음 흐름 →</a>' if index < len(PAGES)-1 else '<a href="index.html">개념·운영 문서 →</a>'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(page["num"] + " · " + page["title"])} · TRACEBACK</title><style>{STYLE}</style></head>
<body><main><nav class="top" aria-label="문서 탐색"><a href="index.html">← TRACEBACK 전체 구조</a><button type="button" onclick="window.print()">PDF로 저장</button></nav>
<header class="hero"><p class="eyebrow">TRACEBACK 실제 구성 · {page["num"]} / 05 · {escape(page["kicker"])}</p><h1>{escape(page["title"])}</h1><p class="lead">{escape(page["lead"])}</p></header>
<section class="panel" aria-labelledby="flow-title"><h2 id="flow-title">한눈에 보는 경로</h2><ol class="flow" aria-label="{escape(page["caption"])}">{nodes}</ol><p class="caption">{escape(page["caption"])}</p></section>
<section class="panel" aria-labelledby="status-title"><h2 id="status-title">현재 확인 범위</h2><p class="status">{escape(page["status"])}</p></section>
<section class="panel" aria-labelledby="more-title"><h2 id="more-title">이 그림을 이해하거나 확인하려면</h2><ul class="links">{links}</ul><p class="source-note">코드 링크: backend development {BACKEND[:12]} · client development {CLIENT[:12]}. AWS·Vercel 콘솔 상태는 코드와 별도이며, 이전 관찰 날짜를 표시했습니다.</p></section>
<nav class="next" aria-label="앞뒤 흐름">{prev_link}{next_link}</nav></main><script src="feedback.js" defer></script></body></html>
'''


for index, page in enumerate(PAGES):
    (ROOT / page["file"]).write_text(render(page, index))
