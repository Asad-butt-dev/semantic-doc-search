# Notes

Working notes for the semantic search project.
Not documentation — this is for decisions, dead ends, and open questions.

---

## Decisions

Format: what was decided, why, and what the evidence was.

### 2026-08-18 — Naming cleanup and version control
Renamed variables and functions across backend and frontend to follow PEP 8
(snake_case) and TypeScript conventions (camelCase, PascalCase for types).
Field names unified to English across chunk dicts, API params, and the
TypeScript interface. Added return type annotations and a `Chunk` TypedDict.
Data paths moved to a `DATA_DIR` constant built from `Path(__file__).parent`.
Set up git and pushed to GitHub.

### 2026-08-17 — React frontend working end to end
Rebuilt the plain-JS search form in React + TypeScript. Four controlled inputs
(one checkbox using `checked` instead of `value`), results held in a typed
state array, rendered with `.map()` and a `key` of filename + chunk number.
Fetch logic is unchanged from the plain version — only the source of the values
(state instead of DOM) and the destination of the result (setState instead of
innerHTML) differ.

### 2026-08-16 — Cosine similarity implemented manually
Wrote the dot-product / norm calculation with numpy instead of using a vector
database. Reason: 33 chunks, no need for an index structure. Also wanted to
understand what the libraries actually do.
Trade-off: does not scale past a few thousand chunks.

### 2026-08-16 — Hybrid search as a score bonus, not a filter
First idea was to zero out embedding rows for chunks without the term.
Rejected: zero vectors break the cosine (division by zero → NaN), and it turns
a soft ranking into a hard filter. Instead: cosine score + weight * term_hit.
Weight is a tunable parameter, still needs to be optimised against eval set.

### 2026-08-16 — Kept plain HTML frontend alongside React
Moved to `frontend-plain/`. Useful as a comparison to see what React actually
adds.

<!-- Template:
### YYYY-MM-DD — <decision in one line>
What: 
Why: 
Evidence / measurement: 
Trade-off: 
-->

---

## Measurements

| Date | Model | Chunk size | Overlap | Hybrid weight | Recall@5 | Notes |
|------|-------|-----------|---------|---------------|----------|-------|
| | paraphrase-multilingual-MiniLM-L12-v2 | 500 | 50 | 0.0 | ? | baseline, not yet measured |
| | | | | | | |

Eval set: `eval.json`, N questions, target = correct source file in top 5.
Questions deliberately avoid the exact wording used in the slides.

---

## Time spent

Rough tracking — useful for estimating the next project.

| Day | Task | Estimated | Actual |
|-----|------|-----------|--------|
| 1 | Extraction, chunking, embeddings | — | |
| 2 | Search, persistence, eval skeleton | — | |
| 3 | FastAPI + plain JS frontend | 7–10 h | done in one day |
| | | | |

---

## Time sinks (and the fix)

Things that cost more than 30 minutes. These come back.

- **Renaming the project folder broke the venv.** Absolute paths are baked in,
  so `pip freeze` came back empty and pip resolved to an empty environment.
  Fix: delete `venv/`, recreate, reinstall. Lesson: generate
  `requirements.txt` *before* moving or renaming anything.
- **First `git add .` picked up `venv/`.** `.gitignore` wasn't taking effect.
  `git rm -r --cached .` undoes staging without touching files.

- **Node version too old for Vite.** Error said "cannot find native binding /
  npm bug, delete node_modules" — misleading. Real cause was in the
  `EBADENGINE` warnings further up: Node 20.18 installed, Vite needs 20.19+.
  Fix: update Node, reopen terminal, delete the half-scaffolded folder, rerun.
- **422 from FastAPI on every request.** Param name in the frontend (`q`) did
  not match the Python signature (`qu`). The 422 response body says exactly
  which field is missing — `loc: ['query', 'qu']`. Read the response body, not
  just the server log.
- **Checkbox always sent `on`.** Checkboxes use `.checked` (boolean), not
  `.value` (which is the literal string `"on"`). Only element where this
  differs.
- **PowerShell blocked venv activation.** `Set-ExecutionPolicy RemoteSigned
  -Scope CurrentUser`.
- **CORS finally triggered with Vite on :5173.** Never appeared with the plain
  HTML frontend (file:// origin). Fixed with FastAPI's `CORSMiddleware`.
  Note: `localhost` and `127.0.0.1` count as different origins — the allowed
  origin must match exactly what the browser shows.
---

## Open questions

Things that work but I don't fully understand yet, or haven't tested.

- [ ] MiniLM has a 128-token limit — are 500-word chunks silently truncated?
      Test 100 vs 500 word chunks against the eval set.
- [ ] E5 models need `query:` / `passage:` prefixes. Would
      `encode_query` / `encode_document` handle this automatically?
- [ ] Scores currently exceed 1.0 because the term bonus is added on top of
      the cosine. Should cosine and bonus be returned separately?
- [] Empty query still returns results (pure bonus matches). Guard in the
      frontend, or reject server-side?
- [X] CORS never triggered with the plain HTML frontend. Was the middleware
      already added, or was it the `file://` origin? Will show up with Vite
      on port 5173.
- [ ] With the term bonus active, all top results came from a single file.
      Does the bonus crowd out good matches from other documents? Check
      against the eval set.

---

## Known limitations

For the README later — being explicit about these is worth more than hiding them.

- Lecture slides are poor source material: 34 pages yielded ~970 words.
  Formulas and diagrams are invisible to text extraction, so mathematical
  content is effectively unsearchable.
- Scanned PDFs without a text layer are skipped entirely, not OCR'd.
- Linear scan over all chunks per query — fine at this scale, not beyond.