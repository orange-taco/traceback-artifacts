"""Render the single Pages entry point from the subject/topic catalog."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


SITE = Path(__file__).resolve().parents[1] / "docs" / "artifact"
CATALOG = SITE / "catalog.json"
OUTPUT = SITE / "index.html"
INDEX_STYLES = SITE / "styles" / "index.css"


def load_catalog() -> dict:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    collections = catalog["collections"]
    subjects = catalog["subjects"]
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    collection_ids: set[str] = set()
    for collection in collections:
        collection_id = collection["id"]
        if collection_id in collection_ids:
            raise ValueError(f"duplicate collection id: {collection_id}")
        collection_ids.add(collection_id)
    for subject in subjects:
        subject_id = subject["id"]
        if subject_id in seen_ids:
            raise ValueError(f"duplicate subject id: {subject_id}")
        seen_ids.add(subject_id)
        if subject["collection"] not in collection_ids:
            raise ValueError(
                f"unknown collection for subject {subject_id}: {subject['collection']}"
            )
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
    return catalog


def render(catalog: dict) -> str:
    collections = catalog["collections"]
    subjects = catalog["subjects"]
    collection_subjects = {
        collection["id"]: [
            subject for subject in subjects if subject["collection"] == collection["id"]
        ]
        for collection in collections
    }
    total_topics = sum(len(subject["topics"]) for subject in subjects)
    total_artifacts = sum(
        len(topic["artifacts"])
        for subject in subjects
        for topic in subject["topics"]
    )
    style_version = sha256(INDEX_STYLES.read_bytes()).hexdigest()[:12]
    nav = "".join(
        f'<a href="#collection-{escape(collection["id"])}">{escape(collection["title"])}</a>'
        for collection in collections
    )
    routes: list[str] = []
    sections: list[str] = []
    filters = ['<button type="button" data-collection-filter="all" aria-pressed="true">전체</button>']
    for collection in collections:
        grouped_subjects = collection_subjects[collection["id"]]
        subject_count = len(grouped_subjects)
        artifact_count = sum(
            len(topic["artifacts"])
            for subject in grouped_subjects
            for topic in subject["topics"]
        )
        routes.append(
            f'<a class="route-card route-{escape(collection["id"])}" '
            f'href="#collection-{escape(collection["id"])}">'
            f'<span class="route-label">{escape(collection["label"])}</span>'
            f'<strong>{escape(collection["title"])}</strong>'
            f'<p>{escape(collection["description"])}</p>'
            f'<small>{subject_count}개 주제 · {artifact_count}개 문서</small></a>'
        )
        filters.append(
            f'<button type="button" data-collection-filter="{escape(collection["id"])}" '
            f'aria-pressed="false">{escape(collection["title"])}</button>'
        )
        rendered_subjects: list[str] = []
        for subject in grouped_subjects:
            topics: list[str] = []
            subject_artifacts = sum(len(topic["artifacts"]) for topic in subject["topics"])
            for topic in subject["topics"]:
                reading_path = topic.get("layout") == "reading-path"
                cards_class = "cards reading-path" if reading_path else "cards"
                cards_attrs = ' role="group" aria-label="추천 읽기 순서"' if reading_path else ""
                cards: list[str] = []
                for index, item in enumerate(topic["artifacts"], start=1):
                    card_label = f"STEP {index:02d}" if reading_path else "GUIDE"
                    search_text = " ".join(
                        [
                            collection["title"],
                            subject["title"],
                            topic["title"],
                            item["title"],
                            item["description"],
                        ]
                    )
                    cards.append(
                        f'<a class="card" href="{escape(item["href"])}" '
                        f'data-search="{escape(search_text)}">'
                        f'<span class="card-label">{card_label}</span>'
                        f'<strong>{escape(item["title"])}</strong>'
                        f'<span class="card-description">{escape(item["description"])}</span>'
                        f'<span class="card-open">열기 <b aria-hidden="true">→</b></span></a>'
                    )
                topics.append(
                    f'<section class="topic" id="{escape(subject["id"])}-{escape(topic["id"])}">'
                    f'<div class="topic-head"><div><span>TOPIC</span><h4>{escape(topic["title"])}</h4></div>'
                    f'<p>{escape(topic["description"])}</p></div>'
                    f'<div class="{cards_class}"{cards_attrs}>{"".join(cards)}</div></section>'
                )
            rendered_subjects.append(
                f'<details class="subject" id="{escape(subject["id"])}" open>'
                f'<summary><span><small>SUBJECT</small><strong>{escape(subject["title"])}</strong>'
                f'<em>{escape(subject["description"])}</em></span>'
                f'<b>{len(subject["topics"])}개 분야 · {subject_artifacts}개 문서</b></summary>'
                f'<div class="subject-body">{"".join(topics)}</div></details>'
            )
        sections.append(
            f'<section class="collection collection-{escape(collection["id"])}" '
            f'id="collection-{escape(collection["id"])}" data-collection="{escape(collection["id"])}">'
            f'<header class="collection-head"><div><p class="eyebrow">{escape(collection["label"])}</p>'
            f'<h2>{escape(collection["title"])}</h2></div>'
            f'<p>{escape(collection["description"])}</p>'
            f'<span>{subject_count}개 주제 · {artifact_count}개 문서</span></header>'
            f'{"".join(rendered_subjects)}</section>'
        )
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="TRACEBACK 프로젝트 구현 문서와 독립적인 개념 학습 자료를 구분해 탐색하는 아티팩트 허브">
<title>TRACEBACK 아티팩트 허브</title>
<link rel="stylesheet" href="styles/index.css?v={style_version}"></head><body><button class="pdf" type="button" onclick="window.print()">PDF로 저장</button><main>
<nav class="top" aria-label="페이지 바로가기"><a class="brand" href="#top">TRACEBACK · ARTIFACTS</a><div>{nav}</div></nav>
<header class="hero" id="top"><div><p class="eyebrow">KNOWLEDGE HUB</p><h1>프로젝트와 공부를<br>한눈에, 따로 읽기</h1><p>실제 TRACEBACK 구현 기록과 독립적인 개념 학습 자료를 분리했습니다. 목적에 맞는 입구를 고른 뒤, 분야별 읽기 순서를 따라가세요.</p></div><div class="hero-stats" aria-label="문서 현황"><span><strong>{len(subjects)}</strong>주제</span><span><strong>{total_topics}</strong>분야</span><span><strong>{total_artifacts}</strong>문서</span></div></header>
<section class="routes" aria-labelledby="routes-heading"><div class="routes-head"><p class="eyebrow">CHOOSE A PATH</p><h2 id="routes-heading">무엇을 찾고 있나요?</h2><p>프로젝트의 현재 상태를 확인하는 문서와, 원리를 공부하는 문서를 섞지 않았습니다.</p></div><div class="route-grid">{"".join(routes)}</div></section>
<section class="catalog-tools" aria-label="문서 필터와 검색"><div class="filters" role="group" aria-label="문서 유형 필터">{"".join(filters)}</div><div class="search-wrap"><label for="artifact-search">문서 찾기</label><input class="search" id="artifact-search" type="search" placeholder="예: 배포, 로그인, MVCC, 잠금" autocomplete="off"></div><p id="result-count" role="status" aria-live="polite">전체 {total_artifacts}개 문서</p></section>
<div id="catalog">{"".join(sections)}</div><p id="search-empty" hidden>조건에 맞는 문서가 없습니다. 검색어 또는 분류 필터를 바꿔 보세요.</p>
<footer class="foot">GitHub Pages의 공개 문서입니다. AWS·Vercel 상태는 각 문서의 확인 날짜를 기준으로 읽으세요.</footer>
</main><script src="feedback.js" defer></script><script>
const search=document.getElementById('artifact-search');const cards=[...document.querySelectorAll('.card')];const filterButtons=[...document.querySelectorAll('[data-collection-filter]')];let activeCollection='all';
function applyFilters(){{const q=search.value.trim().toLocaleLowerCase();let visibleCount=0;document.body.classList.toggle('is-searching',!!q);for(const collection of document.querySelectorAll('.collection')){{const collectionAllowed=activeCollection==='all'||collection.dataset.collection===activeCollection;for(const card of collection.querySelectorAll('.card')){{const matches=collectionAllowed&&(!q||card.dataset.search.toLocaleLowerCase().includes(q));card.hidden=!matches;if(matches)visibleCount++}}for(const topic of collection.querySelectorAll('.topic')){{topic.hidden=![...topic.querySelectorAll('.card')].some(card=>!card.hidden)}}for(const subject of collection.querySelectorAll('.subject')){{subject.hidden=![...subject.querySelectorAll('.topic')].some(topic=>!topic.hidden);if(q&&!subject.hidden)subject.open=true}}collection.hidden=!collectionAllowed||![...collection.querySelectorAll('.subject')].some(subject=>!subject.hidden)}}document.getElementById('search-empty').hidden=visibleCount>0;document.getElementById('result-count').textContent=`${{activeCollection==='all'?'전체':filterButtons.find(button=>button.dataset.collectionFilter===activeCollection).textContent}} · ${{visibleCount}}개 문서`}}
search.addEventListener('input',applyFilters);for(const button of filterButtons){{button.addEventListener('click',()=>{{activeCollection=button.dataset.collectionFilter;for(const candidate of filterButtons)candidate.setAttribute('aria-pressed',String(candidate===button));applyFilters()}})}}
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
