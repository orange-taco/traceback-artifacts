# Artifact working rules

This repository owns the TRACEBACK learning HTML, images, and the
`auth-flow-visualizer` skill. The backend source of truth is the separate
`orange-taco/traceback` repository.

Before changing a guide:

1. Read `README.md` and `.codex/skills/auth-flow-visualizer/SKILL.md`.
2. Identify which statements describe general concepts and which describe
   current TRACEBACK code or deployed state.
3. For current-code claims, inspect `orange-taco/traceback` at an identifiable
   revision. In Codex Cloud, attach both repositories to the environment;
   do not assume the reader's iPad has a local checkout. If the backend is
   unavailable, say so and avoid asserting that code or infrastructure is current.
4. Edit only this repository's guides and supporting assets. Link source
   excerpts to the backend repository and revision, with line numbers where
   the skill requires them.
5. Run `python3 scripts/verify_site.py` and inspect the rendered page at a
   narrow and a desktop viewport when the visual layout changes.

The index at `docs/artifact/index.html` is the single entry point. Keep the
five AWS learning guides in their established reading order and preserve the
skill's Required artifact standard.
