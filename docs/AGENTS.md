# Agent Guide

This repository is a single Helm chart for Traefik Kubernetes CRD resources with layered tests under `tests/units`, `tests/smokes`, and `tests/e2e`.

Keep implementation, tests, CI, and docs aligned in the same change. If a resource kind, version pin, or workflow changes, update every place that encodes that assumption.

## Repository Shape

Prefer this baseline structure:

```text
.
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── values.yaml.example
├── templates/
├── tests/
│   ├── fixtures/
│   ├── units/
│   ├── smokes/
│   └── e2e/
└── docs/
```

Keep the tree minimal. Do not add parallel structures that solve the same problem twice.

## Documentation Rules

- Keep one root `README.md` as the primary entry point.
- Keep `README.md` generated from `docs/README.md.gotmpl` via `helm-docs` and `pre-commit`.
- Keep test-layer details in `docs/TESTS.MD`.
- Keep local dependency guidance in `docs/DEPENDENCY.md`.
- Use relative repository links in Markdown.
- Document the implemented workflow, not an aspirational one.
- If a workflow is local-only, say so explicitly.
- When changing values, update the `# --` comments in `values.yaml`.

## Chart Design Expectations

- Keep templates thin and deterministic.
- Centralize shared rendering logic in `templates/_helpers.tpl`.
- Prefer the generic resource contract already used by the chart unless there is a strong reason to split behavior.
- Keep defaults minimal; `values.yaml` should render nothing.
- Keep `values.yaml.example` comprehensive enough to exercise every supported kind.
- Avoid managing `status` outside tests and synthetic fixtures.

## Traefik CRD Rules

For this repository, keep these assumptions explicit:

- the chart renders Traefik CRD resources only; it does not install the controller
- the pinned default API versions are derived from the vendored Traefik v3.6 CRD bundle
- all supported resources in the pinned bundle are namespaced
- `apiVersions.*` overrides are part of the public contract
- `tests/fixtures/traefik-crd-definition-v1.yml` is the single upstream source for e2e CRD bootstrap and local schema export

When updating the pinned Traefik version:

- replace the vendored CRD bundle with the exact upstream file
- verify every supported kind still exists and is still namespaced
- re-run smoke validation and local e2e
- update docs and CI version references in the same change

## Test Layers

### Unit Tests

Use `helm-unittest` for chart-owned rendering behavior:

- helper behavior
- label and annotation merges
- namespace handling
- API version overrides
- representative manifests from the example values

### Smoke Tests

Use smoke tests for render-path validation without a live cluster:

- default empty render
- values schema enforcement
- representative example rendering
- `kubeconform` validation using schemas exported from the vendored CRD bundle

### E2E Tests

Use `kind`-based e2e for what the other layers cannot prove:

- CRD registration in a real API server
- end-to-end `helm upgrade --install`
- installability of the example fixtures against the pinned CRDs

Keep e2e local-first unless the actual CI runners can support Docker and kind.

## CI Guidance

CI should cover the lightweight checks by default:

- lint
- unit tests
- smoke tests
- backward compatibility rendering
- manifest rendering
- `kubeconform` validation

Prefer reusing the vendored CRD bundle and the repository's own helper scripts instead of depending on external schema catalogs for Traefik CRDs.

## Makefile Guidance

If the repository ships a `Makefile`, keep it as a thin wrapper around existing scripts:

- `make hooks-install`
- `make docs`
- `make lint`
- `make test-unit`
- `make test-compat`
- `make test-smoke`
- `make test-smoke-fast`
- `make test-e2e`
- `make test-e2e-debug`
- `make test-e2e-help`

## Change Discipline

When making repository-wide changes, prefer this order:

1. update the implementation
2. align tests and fixtures
3. align CI defaults
4. align documentation
5. run a compact verification pass

Do not leave the repository in a state where code, docs, and CI describe different Traefik versions or resource sets.

## Compact Verification

Before finishing a change, prefer to run:

```bash
git diff --check
helm lint . -f values.yaml.example
helm template nuc-traefik . -f values.yaml.example
sh -n tests/units/backward_compatibility_test.sh
bash -n tests/e2e/test-e2e.sh
python3 -m py_compile tests/smokes/helpers/argparser.py tests/smokes/run/smoke.py tests/smokes/scenarios/smoke.py tests/smokes/steps/*.py scripts/export-crd-schemas.py
```
