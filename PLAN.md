# Keysso CLI Plan

Date: 2026-02-17
Scope: only `report -> simple -> context` (without `direct`)

- [x] Verify and lock SDK/OpenAPI contract for `report.simple.context` and subresources (`keywords`, `ads`, `retrieve_concurents`)
- [x] Initialize installable CLI package in `keysso-cli` via `uv` with a console entry point
- [x] Build extensible CLI skeleton aligned with SDK hierarchy: `report -> simple -> context`
- [x] Implement only context commands:
  - [x] `context concurents`
  - [x] `context keywords list`
  - [x] `context keywords byads`
  - [x] `context ads retrieve`
  - [x] `context ads links`
  - [x] `context ads facts`
- [x] Extract shared query options into one parsing layer: `base`, `filter`, `page`, `per-page`, `sort`
- [x] Add unit tests for CLI routing and SDK argument mapping without network calls
- [x] Add a short `README.md` with `uv` install instructions and context command examples
- [x] Run `pytest` and smoke checks for CLI startup and `--help`
