# content/ manifest

One row per file in this directory. A copied file is byte-identical to `path` in `repo` at
`commit`; `scripts/check.py` verifies that against the local checkout when it is present, and
checks every string of the file against each page in `rendered_in` (space-separated built page
files such as `tr/withdrawal.html`, `-` until the first is built; a named page that is missing
fails) (D-2026-09-12-12, D-2026-09-12-15). A file whose `repo` is this repo
is authored here (D-2026-09-12-9). Local checkouts: `kdemirtas/nepsis` at
`~/code/personal/mobile-app/nepsis/`.

| file | repo | commit | path | copied_on | rendered_in |
|---|---|---|---|---|---|
| `PRIVACY.md` | `kdemirtas/nepsis` | `19a1857a212c3b4707b9f806e9e424c3f1c810cc` | `PRIVACY.md` | 2026-09-12 | - |
| `withdrawal-en.json` | `kdemirtas/nepsis` | `19a1857a212c3b4707b9f806e9e424c3f1c810cc` | `sources/withdrawal-en.json` | 2026-09-12 | - |
| `withdrawal-tr.json` | `kdemirtas/nepsis` | `19a1857a212c3b4707b9f806e9e424c3f1c810cc` | `sources/withdrawal-tr.json` | 2026-09-12 | - |
