0a. Study the files in "/Assets/BeziBridge/specs/*" to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md (if present, if not create a page for it) to understand the plan so far.
0c. Study "/Assets/" to understand shared utilities & components.
0d. For reference, the application source code is in "/Assets/_GAME/Scripts/". Create the directory if it doesn't exist. Do the same with other directories needed in _Game: Scripts, Materials, etc.
0e. Place a new documentation in pages located under a @Documentation folder.
0f. New source code should be placed in "/Assets/_Game/Source/".

1. Study @IMPLEMENTATION_PLAN.md (if present; it may be incorrect) and study existing source code and compare it against "/Assets/BeziBridge/specs/*". Analyze findings, prioritize tasks, and create/update @IMPLEMENTATION_PLAN.md as a bullet point list sorted in priority of items yet to be implemented. Consider searching for TODO, minimal implementations, placeholders, skipped/flaky tests, and inconsistent patterns. Study @IMPLEMENTATION_PLAN.md to determine starting point for research and keep it up to date with items considered complete/incomplete.

IMPORTANT: Plan only. Do NOT implement anything. Do NOT assume functionality is missing; confirm with code search first. Treat "/Assets/" as the project's standard library for shared utilities and components. Prefer consolidated, idiomatic implementations there over ad-hoc copies.

ULTIMATE GOAL: We want to achieve a PLAYABLE VIDEO GAME. Consider missing elements and plan accordingly. If an element is missing, search first to confirm it doesn't exist, then if needed author the specification at "/Assets/BeziBridge/specs/game_spec.md. If you create a new element then document the plan to implement it in @IMPLEMENTATION_PLAN.md.
