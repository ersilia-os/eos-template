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

- Read `input_file = sys.argv[1]`, `output_file = sys.argv[2]`. No other CLI flags.
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

- `model/checkpoints/` and `model/framework/fit/` are gitignored on purpose. Never `git add` them.
- Persist them with [`eosvc`](https://github.com/ersilia-os/eosvc), which backs both folders with S3.
- `access.json` controls public vs. private — both default to public. Only change on explicit user request.

## Versioning

Models follow [semantic versioning](https://semver.org/) (`vMAJOR.MINOR.PATCH`) via git tags / GitHub releases — the `retag-release-docker.yml` workflow propagates the tag to the published Docker image.

- **MAJOR** — any change a downstream user can observe in the predictions. New, removed, or renamed columns in `run_columns.csv`; a different dtype; retrained checkpoints; an upstream library bump that shifts predicted values. If, for fixed-output models, `examples/run_output.csv` is no longer reproducible byte-for-byte with the previous release on the same `run_input.csv`, it's MAJOR.
- **MINOR** — additive, output-preserving changes (new optional metadata, expanded examples, faster implementation that produces identical values).
- **PATCH** — fixes that do not change predictions: docs, install.yml pin nudges that still resolve to the same wheels, CI-only tweaks.

Never change version without asking the user.

## GitHub Actions workflows

The workflows in `.github/workflows/` are thin wrappers around reusable workflows in [`ersilia-os/ersilia-model-workflows`](https://github.com/ersilia-os/ersilia-model-workflows) — that's where the actual test, S3 upload, and Docker pack logic lives. Read it there before debugging CI behaviour, and do not edit the local YAMLs to work around a failure.

- **Open a PR; don't push to `main`.** `test-model-pr.yml` gives a fast signal on a PR. `upload-model.yml` runs on push to `main` and chains `test-model-source` → `upload-model-to-s3` → `upload-ersilia-pack`; a broken model wastes S3/DockerHub budget.
- **A model isn't done until every workflow is green.** Status: PR test, source test, S3 upload, ersilia-pack image build, image test.
- **Inspect failures with `gh`.** `gh run list --limit 5`, then `gh run view <id> --log-failed`. Reproduce the failure locally (run `run.sh` against `examples/run_input.csv` and diff against `run_output.csv`) before pushing a fix.
- **Re-running uploads.** `upload-model.yml` supports `workflow_dispatch` — after merging a fix to `main`, trigger it manually rather than pushing an empty commit.

## Ersilia ecosystem

Be aware of the rest of the org at [github.com/ersilia-os](https://github.com/ersilia-os) — in particular [`ersilia`](https://github.com/ersilia-os/ersilia), [`ersilia-pack`](https://github.com/ersilia-os/ersilia-pack), [`ersilia-pack-utils`](https://github.com/ersilia-os/ersilia-pack-utils), and [`eosvc`](https://github.com/ersilia-os/eosvc). Skills in [`ersilia-skills`](https://github.com/ersilia-os/ersilia-skills) are updated independently — check it before writing the same logic from scratch.
