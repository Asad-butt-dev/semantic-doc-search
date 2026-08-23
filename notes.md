# Notes

Working notes for the semantic search project.
Not documentation — this is for decisions, dead ends, and open questions.

---

## Decisions
### 2026-08-20 — Model comparison: MiniLM-multi vs E5-base

Ran both models across ten chunk sizes (200–650 words), 100 queries, hybrid off.

E5-base wins at **every single chunk size** — 10 out of 10, on all three
metrics. Individual differences sit near one standard error (~0.03 at n=100)
and would not be convincing alone, but a clean sweep of ten paired comparisons
is. Averaged over all sizes: Recall@1 +6.2pp, Recall@5 +3.2pp, MRR +5.7pp.

**The truncation hypothesis holds up, partially.** E5 (512 tokens ≈ 350–400
English words) peaks at chunk size 350 and declines steadily beyond it:
Recall@1 falls 0.85 → 0.77 from 350 to 650, MRR 0.885 → 0.819. The decline
begins roughly where the context window runs out. It is a gradual slope rather
than a sharp knee, so the effect is visible but not dramatic.

MiniLM-multi (128 tokens ≈ 90 words) shows no trend at all across chunk sizes,
only noise. That is consistent: every size tested exceeds its window, so chunk
size only changes how many chunks exist, not how much of each one is encoded.
This explains why the first chunk-size experiment produced nothing — the
variable being tested had no room to act.

Both models peak nominally at 350. For E5 there is a mechanism behind it; for
MiniLM it is most likely coincidence.

**Caveat:** two variables differ between the models — context window and
training corpus. The gain cannot be attributed to window size alone. A cleaner
isolation would need two models of the same family differing only in window
length.

Format: what was decided, why, and what the evidence was.
### 2026-08-19 — First evaluation run

Baseline established: Recall@1 = 0.730, Recall@5 = 0.870, MRR = 0.785 over
100 queries, chunk size 200, hybrid search off. Purely semantic — no lexical
matching involved.

Metrics chosen deliberately. Accuracy is meaningless here: with ~600 chunks
and one correct answer per query, always predicting "not relevant" would score
above 99%. Precision@5 carries no extra information either, since exactly one
file is correct — it is just Recall@5 divided by 5. Recall@1, Recall@5 and MRR
each say something different: whether the top hit is right, whether the answer
is reachable at all, and how well it is ranked in between.

MRR is computed at file level: walk the ranked results, take 1/position of the
first hit from the target file, 0 if none. Averaged over all queries.

Random baseline for context: with 20 files, Recall@5 by chance would sit near
0.25.

**Known distortion:** MiniLM truncates at 128 tokens — roughly 90 English
words. Every chunk size tested (200–650 words) exceeds this, so at 650 only
the first ~15% of a chunk is actually encoded. The chunk size comparison
therefore measures how much text is *lost*, not how chunking affects
retrieval. A model with a 512-token window (e.g. multilingual-e5-base) is
needed to make that experiment meaningful.

### 2026-08-19 — Evaluation set

100 queries over the 20 most recently added PDFs. All 20 files are
represented, with an uneven number of questions per file; order is shuffled.

**Generated with an LLM** (PDFs supplied as context), then reviewed by hand.
Not written from scratch — worth knowing when reading the numbers.

Design goal: each question should be answerable from its labelled
`file_name` and not equally well from another PDF in the corpus. This matters
for the overlapping topics — SVM, CTL/bisimulation, dimensionality reduction —
where a generic question would have several valid sources and a correct
retrieval would be scored as a miss. Handled by anchoring questions to
material unique to each file: logistic regression content for lecture 8,
soft-margin and hinge loss for lecture 9.
Fields per entry: `query`, `file_name`, `content_type`
(conceptual / formula), `specificity` (broad / specific).

**Caveat:** the questions are LLM-generated, so their phrasing may sit closer
to the source wording than a human's would — which would inflate scores by
testing lexical rather than semantic matching. Something to watch when
interpreting the hybrid-search results in particular.

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

| Date | Model | Chunk size | Overlap | Hybrid | Recall@1 | Recall@5 | MRR | Notes |
|------|-------|-----------|---------|--------|----------|----------|-----|-------|
| Date | Model | Max tokens | Chunk size | Hybrid | Recall@1 | Recall@5 | MRR | Notes |
|------|-------|-----------|-----------|--------|----------|----------|-----|-------|
| 2026-08-20 | paraphrase-multilingual-MiniLM-L12-v2 | 128 | 350 | off | 0.780 | 0.910 | 0.828 | best of 10 sizes |
| 2026-08-20 | paraphrase-multilingual-MiniLM-L12-v2 | 128 | — | off | 0.743 | 0.884 | 0.794 | mean over 200–650 |
| 2026-08-20 | intfloat/multilingual-e5-base | 512 | 350 | off | 0.850 | 0.930 | 0.885 | best of 10 sizes |
| 2026-08-20 | intfloat/multilingual-e5-base | 512 | — | off | 0.805 | 0.916 | 0.851 | mean over 200–650 |


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