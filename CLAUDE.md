# Ersilia Model Hub — Model Developer Guide

This is the developer guide for a model built from the [`eos-template`](https://github.com/ersilia-os/eos-template) scaffold. It complements `README.md`, which is the user-facing onboarding doc and is **automatically overwritten** when the model is incorporated into the Hub — durable agent rules live here, not in `README.md`.

Background reading: [Ersilia model contribution docs](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/) and the [model template page](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template).

## Working with the user

- **Ask, don't assume.** For any non-trivial decision — which approach to take, what to name something, whether to add a dependency, how to handle an ambiguous case — use `AskUserQuestion` BEFORE editing.
- **Plans are mandatory.** Anything beyond a one-line fix or pure read-only investigation must go through plan mode. If invoked outside plan mode for non-trivial work, propose a plan and stop until the user confirms.
- **Surface uncertainty.** When you have multiple reasonable options or are unsure about intent, name them and ask. Don't pick silently.

## Don't touch

- `README.md` is regenerated on incorporation — do not hand-edit it.
- The `model/` folder tree is fixed. Do not add new top-level folders, rename `framework/`, `checkpoints/`, `examples/`, `columns/`, or move `run.sh`.
- The metadata fields populated by CI (contributor, S3 paths, DockerHub paths, computational performance, incorporation date) are owned by the workflows. Never hand-edit them.

## `model/framework/run.sh`

Mandatory. Receives three arguments from Ersilia: `$1` framework dir, `$2` input CSV, `$3` output CSV. The default body is `python $1/code/main.py $2 $3`. The presence of `run.sh` is what tells Ersilia the model exposes a `run` API — do not rename or remove it. Use absolute paths only via `$1`.

## `model/framework/code/main.py`

- Split the code into two top-level functions so the model can be served warm (loaded once, reused across batches):
  - `load_tool()` does everything slow and batch-independent (heavy imports, reading checkpoints, building the model) and returns the loaded model.
  - `run_tool(model, input_file, output_file)` processes one batch: `read_smiles`, predict, `write_out`. It must not reload anything and must not depend on state left over from earlier batches.
- Keep the `if __name__ == "__main__":` block that reads `input_file = sys.argv[1]`, `output_file = sys.argv[2]` and calls `run_tool(load_tool(), input_file, output_file)`. `run.sh`, `ersilia test` and CI still execute `main.py` as a script. No other CLI flags, and no work at module level outside the functions and constants.
- Warm serving only applies when `run.sh` is the default single line `python $1/code/main.py $2 $3`. Any other `run.sh` keeps running once per batch.
- Use `from ersilia_pack_utils.core import read_smiles, write_out` (already pinned in `install.yml`) — do not hand-roll csv parsing. `read_smiles` returns `(header, smiles_list)` and transparently handles `.csv` and `.bin` inputs.
- Write outputs with `write_out(results, header, output_file, dtype)`. Allowed dtypes: `np.float32` or `np.int32`. NaNs and inf are clipped automatically.
- Column headers must exactly match `model/framework/columns/run_columns.csv`. Conventions: `feat_000`, `feat_001`, … for featurizers; `smi_00`, `smi_01`, … for generators; descriptive `snake_case` for scalar predictors.
- Resolve checkpoint paths from `os.path.dirname(__file__)` — do not hardcode absolute paths.

## `install.yml`

- Pin **exact** versions for every entry. CI rebuilds break when floors or unpinned ranges drift.
- Prefer `pip` over `conda`. Reach for `conda` only when no PyPI wheel exists for the platform.
- Keep the dependency list minimal — extra packages produce solver conflicts during the Docker pack build.

## `metadata.yml`

- Most fields are enumerations matched against fixed lists. Exact casing and spelling matter or the metadata check fails. Check the [model template docs](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template) for valid values before guessing.
- Multi-value fields (`Task`, `Subtask`, `Input`, `Output`, `Tag`, `Biomedical Area`, `Target Organism`) stay as YAML lists.
- `Status` starts as `In progress`. CI flips it later.

## Examples and columns

- `examples/run_input.csv` (generate with `ersilia example`) and `examples/run_output.csv` are both mandatory. Regenerate them together whenever `main.py` or the output schema changes — never edit one without the other.
- `columns/run_columns.csv` needs name + type (`float`/`integer`/`string`) + direction (`high`/`low` or empty) + a one-sentence description for each output column.

## Checkpoints and `eosvc`

Full rule: [Checkpoints and storage](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template#checkpoints-and-storage) in the Ersilia Book.

- Weights the model loads at inference live in `model/checkpoints/`, never in `model/framework/code/`. The model must not download weights at run time (Hugging Face, Google Drive, Zenodo…): download once, place them in `model/checkpoints/`, load from there.
- `model/checkpoints/` is committed to git if every file is under 100 MiB (104,857,600 bytes, GitHub's limit). Check with `find model/checkpoints -type f -size +104857599c`; any output means the whole folder goes to `eosvc`.
- `model/framework/fit/` goes to [`eosvc`](https://github.com/ersilia-os/eosvc) as soon as it holds training code or data, whatever its size. A model without a training step keeps the template skeleton (`README.md` and the `.gitkeep` folders) in git and does not list `fit` in `access.json` or `.gitignore`.
- To store a folder with `eosvc`: list it in `access.json` (e.g. `{"checkpoints": "public", "fit": "public"}`), add it under a `#eosvc managed` block in `.gitignore` (`model/checkpoints/*`, `model/framework/fit/*`), and run `eosvc upload --path checkpoints` / `--path fit`. Never `--path .`, which uploads both folders. Leaving a folder out of `access.json` does not protect it: eosvc treats a missing key as public, and CI runs `eosvc download --path .` whenever `access.json` exists.
- No Git LFS: no `.gitattributes` LFS rules, no `mock.csv`/`mock.txt`.
- Never keep a folder in both git and S3: when `access.json` exists, CI downloads the S3 copy over the git one. If a folder was committed before moving it to eosvc, untrack it with `git rm -r --cached model/checkpoints` (or `model/framework/fit`).
- `access.json` controls public vs. private — public by default. Only change on explicit user request.

## Versioning

Models follow [semantic versioning](https://semver.org/) (`vMAJOR.MINOR.PATCH`) via GitHub releases — the `retag-release-docker.yml` workflow propagates the tag to the published Docker image. The rules and the pre-release checklist are in [Model releases](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/example-of-the-model-incorporation-workflow#model-releases) in the Ersilia Book; in short:

- **MAJOR** — checkpoints change; output columns added, removed, renamed, reordered or retyped; inputs that returned a value now return empty; values for valid inputs change beyond 1e-4 (whatever the cause); for generators, a new sampling method, model or selection criteria.
- **MINOR** — code, dependency or image changes with the same columns and outputs within 1e-4: dependency updates and the rebuilds they need, speed-ups, smaller images, a GPU option (GPU outputs may differ slightly; report the difference), fixes where failing inputs now return a result, the same weights in another file format, moving checkpoints into `model/checkpoints/`.
- **PATCH** — no change to code, dependencies, checkpoints or outputs: metadata, README, `run_columns.csv` descriptions or direction, a rebuilt image of unchanged code.
- **No release** — a pure storage move between Git LFS, Git and eosvc, or removing a duplicate copy, with identical files (check every sha256), code and outputs; wait for the PR test, then merge with `[skip ci]`.

Never change version without asking the user.

## GitHub Actions workflows

The workflows in `.github/workflows/` are thin wrappers around reusable workflows in [`ersilia-os/ersilia-model-workflows`](https://github.com/ersilia-os/ersilia-model-workflows) — that's where the actual test, S3 upload, and Docker pack logic lives. Read it there before debugging CI behaviour, and do not edit the local YAMLs to work around a failure.

- **Open a PR; don't push to `main`.** `test-model-pr.yml` gives a fast signal on a PR. `upload-model.yml` runs on push to `main` and chains `test-model-source` → `upload-model-to-s3` → `upload-ersilia-pack`; a broken model wastes S3/DockerHub budget.
- **A model isn't done until every workflow is green.** Status: PR test, source test, S3 upload, ersilia-pack image build, image test. Check every job of "Test model image", not only the run: a green run can hide a failed `test-image-arm64`. `test-image-amd64`, `retag-image` and `post-model-upload` must pass. `test-image-arm64` should pass; if the model cannot run on ARM64 for now, set `Docker Architecture` to AMD64 only in the metadata and say so in the release notes.
- **Never "Re-run jobs" on "Test model image" after `post-model-upload` has pushed the metadata once** — the re-run checks out the old commit and its push is rejected. Start a fresh run instead (see the next point).
- **Inspect failures with `gh`.** `gh run list --limit 5`, then `gh run view <id> --log-failed`. Reproduce the failure locally (run `run.sh` against `examples/run_input.csv` and diff against `run_output.csv`) before pushing a fix.
- **Re-running uploads.** `upload-model.yml` supports `workflow_dispatch` — after merging a fix to `main`, trigger it manually rather than pushing an empty commit.

## Ersilia ecosystem

Be aware of the rest of the org at [github.com/ersilia-os](https://github.com/ersilia-os) — in particular [`ersilia`](https://github.com/ersilia-os/ersilia), [`ersilia-pack`](https://github.com/ersilia-os/ersilia-pack), [`ersilia-pack-utils`](https://github.com/ersilia-os/ersilia-pack-utils), and [`eosvc`](https://github.com/ersilia-os/eosvc). Skills in [`ersilia-skills`](https://github.com/ersilia-os/ersilia-skills) are updated independently — check it before writing the same logic from scratch.
