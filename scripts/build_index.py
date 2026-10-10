"""Render the single Pages entry point from the subject/topic catalog."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


SITE = Path(__file__).resolve().parents[1] / "docs" / "artifact"
CATALOG = SITE / "catalog.json"
OUTPUT = SITE / "index.html"


def load_catalog() -> list[dict]:
    subjects = json.loads(CATALOG.read_text(encoding="utf-8"))["subjects"]
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for subject in subjects:
        subject_id = subject["id"]
        if subject_id in seen_ids:
            raise ValueError(f"duplicate subject id: {subject_id}")
        seen_ids.add(subject_id)
        for topic in subject["topics"]:
            topic_id = f"{subject_id}-{topic['id']}"
            if topic_id in seen_ids:
                raise ValueError(f"duplicate topic id: {topic_id}")
            seen_ids.add(topic_id)
            for item in topic["artifacts"]:
                href = item["href"]
                url = urlsplit(href)
                if url.scheme or url.netloc or href.startswith("/") or ".." in Path(url.path).parts:
                    raise ValueError(f"catalog path must be inside docs/artifact: {href}")
                target = (SITE / url.path).resolve()
                if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                    raise ValueError(f"catalog target missing: {href}")
                if href in seen_paths:
                    raise ValueError(f"duplicate catalog artifact: {href}")
                seen_paths.add(href)
    return subjects


def render(subjects: list[dict]) -> str:
    nav = "".join(
        f'<a href="#{escape(subject["id"])}">{escape(subject["title"])}</a>'
        for subject in subjects
    )
    sections: list[str] = []
    for subject in subjects:
        topics: list[str] = []
        for topic in subject["topics"]:
            cards = "".join(
                f'<a class="card" href="{escape(item["href"])}" '
                f'data-search="{escape(" ".join([subject["title"], topic["title"], item["title"], item["description"]]))}">'
                f'<strong>{escape(item["title"])}</strong><span>{escape(item["description"])}</span></a>'
                for item in topic["artifacts"]
            )
            topics.append(
                f'<div class="topic" id="{escape(subject["id"])}-{escape(topic["id"])}">'
                f'<div class="topic-head"><h3>{escape(topic["title"])}</h3><p>{escape(topic["description"])}</p></div>'
                f'<div class="cards">{cards}</div></div>'
            )
        sections.append(
            f'<section class="subject" id="{escape(subject["id"])}">'
            f'<div class="subject-head"><p class="eyebrow">SUBJECT · {escape(subject["id"])}</p>'
            f'<h2>{escape(subject["title"])}</h2><p>{escape(subject["description"])}</p></div>'
            f'{"".join(topics)}</section>'
        )
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="TRACEBACK 인프라와 계정, 아티팩트 운영을 실제 설정 순서대로 읽는 학습 문서 목차">
<title>학습 아티팩트 · TRACEBACK</title>
<link rel="stylesheet" href="styles/index.css"></head><body><button class="pdf" type="button" onclick="window.print()">PDF로 저장</button><main>
<header class="hero"><p class="eyebrow">LEARNING ARTIFACTS</p><h1>실제 구성을 따라 읽는 아티팩트</h1><p>지금은 TRACEBACK의 인프라와 계정, 이 문서 사이트의 운영 과정을 담았습니다. 각 문서는 설정과 선택 이유를 먼저 보여주고, 그 단계에서 필요한 용어와 코드를 같은 화면에서 설명합니다.</p></header>
<nav class="jump" aria-label="주제 바로가기">{nav}</nav><label for="artifact-search">문서 찾기</label><input class="search" id="artifact-search" type="search" placeholder="주제, 설정, 용어 검색" autocomplete="off">
<div id="catalog">{"".join(sections)}</div><p id="search-empty" hidden>일치하는 문서가 없습니다.</p>
<footer class="foot">GitHub Pages의 공개 문서입니다. AWS·Vercel 상태는 각 문서의 확인 날짜를 기준으로 읽으세요.</footer>
</main><script src="feedback.js" defer></script><script>
const search=document.getElementById('artifact-search');const cards=[...document.querySelectorAll('.card')];
search.addEventListener('input',()=>{{const q=search.value.trim().toLocaleLowerCase();for(const card of cards){{card.hidden=!!q&&!card.dataset.search.toLocaleLowerCase().includes(q)}}for(const topic of document.querySelectorAll('.topic')){{topic.hidden=![...topic.querySelectorAll('.card')].some(card=>!card.hidden)}}for(const subject of document.querySelectorAll('.subject')){{subject.hidden=![...subject.querySelectorAll('.topic')].some(topic=>!topic.hidden)}}document.getElementById('search-empty').hidden=cards.some(card=>!card.hidden)}});
</script></body></html>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if index.html is not regenerated")
    args = parser.parse_args()
    content = render(load_catalog())
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("docs/artifact/index.html is stale; run python3 scripts/build_index.py")
        print("Catalog and index.html match")
    else:
        OUTPUT.write_text(content, encoding="utf-8")
        print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
