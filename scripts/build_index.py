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
    seen_tree_ids: set[str] = set()
    seen_doc_ids: set[str] = set()
    seen_paths: set[str] = set()
    collection_ids: set[str] = set()
    for collection in collections:
        collection_id = collection["id"]
        if collection_id in collection_ids:
            raise ValueError(f"duplicate collection id: {collection_id}")
        collection_ids.add(collection_id)
    for subject in subjects:
        subject_id = subject["id"]
        if subject_id in seen_tree_ids:
            raise ValueError(f"duplicate subject id: {subject_id}")
        seen_tree_ids.add(subject_id)
        if subject["collection"] not in collection_ids:
            raise ValueError(f"unknown collection for subject {subject_id}: {subject['collection']}")
        for topic in subject["topics"]:
            topic_id = f"{subject_id}-{topic['id']}"
            if topic_id in seen_tree_ids:
                raise ValueError(f"duplicate topic id: {topic_id}")
            seen_tree_ids.add(topic_id)
            for item in topic["artifacts"]:
                doc_id = item.get("id")
                if not doc_id or doc_id in seen_doc_ids:
                    raise ValueError(f"missing or duplicate artifact id: {doc_id}")
                seen_doc_ids.add(doc_id)
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


def _counts(subjects: list[dict]) -> tuple[int, int]:
    return (
        sum(len(subject["topics"]) for subject in subjects),
        sum(len(topic["artifacts"]) for subject in subjects for topic in subject["topics"]),
    )


def render(catalog: dict) -> str:
    collections = catalog["collections"]
    subjects = catalog["subjects"]
    total_topics, total_artifacts = _counts(subjects)
    start_cards: list[str] = []
    legacy_anchors: list[str] = []

    for collection in collections:
        grouped = [subject for subject in subjects if subject["collection"] == collection["id"]]
        topic_count, artifact_count = _counts(grouped)
        first_subject = grouped[0]
        first_topic = first_subject["topics"][0]
        first_doc = first_topic["artifacts"][0]
        start_cards.append(
            f'<a class="start-card start-{escape(collection["id"])}" href="{escape(first_doc["href"])}">'
            f'<span>{escape(collection["label"])}</span><strong>{escape(collection["title"])}</strong>'
            f'<p>{escape(collection["description"])}</p>'
            f'<small>시작 문서 · <code>{escape(first_doc["id"])}</code> {escape(first_doc["title"])} <b aria-hidden="true">→</b></small>'
            f'<em>{topic_count}개 주제 · {artifact_count}개 문서</em></a>'
        )
        legacy_anchors.append(f'<span id="view=collection:{escape(collection["id"])}"></span>')

    for subject in subjects:
        legacy_anchors.append(f'<span id="view=subject:{escape(subject["id"])}"></span>')
        for topic in subject["topics"]:
            legacy_anchors.append(f'<span id="view=topic:{escape(subject["id"])}:{escape(topic["id"])}"></span>')

    style_version = sha256(INDEX_STYLES.read_bytes()).hexdigest()[:12]
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="TRACEBACK 프로젝트 문서와 개념 학습 자료를 탐색하는 기술 문서 허브">
<title>TRACEBACK DOCS</title><link rel="stylesheet" href="styles/index.css?v={style_version}"></head>
<body><main><header class="hero"><div><p class="eyebrow">TRACEBACK DOCS</p><h1>트리에서 고르고,<br>문서로 바로 이동</h1><p>상단에서 프로젝트와 개념 학습을 전환하고, 왼쪽에서 분야 → 주제 → 실제 문서를 펼쳐 선택하세요. 중간 소개 화면 없이 문서가 바로 열립니다.</p></div><div class="hero-stats" aria-label="문서 현황"><span><strong>{len(subjects)}</strong>분야</span><span><strong>{total_topics}</strong>주제</span><span><strong>{total_artifacts}</strong>문서</span></div></header>
<section class="nav-guide" aria-labelledby="nav-guide-title"><div><p class="eyebrow">DIRECT NAVIGATION</p><h2 id="nav-guide-title">처음이라면 시작 문서로</h2><p>아래 링크는 각 영역의 첫 문서를 바로 엽니다. 다른 문서는 상단 영역 전환과 왼쪽 문서 트리에서 선택할 수 있습니다.</p></div><div class="start-grid">{"".join(start_cards)}</div></section>
<div class="legacy-anchors" aria-hidden="true">{"".join(legacy_anchors)}</div>
<footer>GitHub Pages의 공개 문서입니다. 실제 환경 상태는 각 문서의 확인 날짜와 근거 revision을 기준으로 읽으세요.</footer></main>
<button class="pdf" type="button" onclick="window.print()">PDF로 저장</button><script src="feedback.js" defer></script></body></html>'''


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
