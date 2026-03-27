# Tests

This chart uses three complementary automated test layers:

- `tests/units/` for fast `helm-unittest` suites and backward-compatibility checks
- `tests/smokes/` for render-path and schema validation without a cluster
- `tests/e2e/` for kind-based chart installation against a real API server with Traefik CRDs

GitLab CI runs linting, unit tests, smoke tests, backward compatibility rendering, full example rendering, and `kubeconform`. The e2e layer remains local-first because it requires Docker and kind.

## Unit Tests

Unit tests live under `tests/units/`.

They focus on chart-owned behavior rather than exhaustively restating Traefik CRD payloads.

### Layout

```text
tests/units/
├── backward_compatibility_test.sh
├── example_resources_test.yaml
├── rendering_contract_test.yaml
└── values/
    └── rendering_contract.values.yaml
```

### Coverage

1. `rendering_contract_test.yaml`
   Verifies the generic rendering helper behavior shared by all templates:
   - `nameOverride`
   - merged labels and annotations
   - namespace fallback
   - explicit namespace override
   - global and per-resource `apiVersion` overrides

2. `example_resources_test.yaml`
   Uses `values.yaml.example` as a representative fixture and checks that:
   - all expected documents are rendered
   - each supported Traefik kind has a stable smoke-level assertion
   - the example stays aligned with the chart contract

3. `backward_compatibility_test.sh`
   Renders the current chart with `values.yaml` from previous stable git tags and verifies that:
   - old values files still pass `helm lint`
   - old values files still render with `helm template`
   - missing previous major, minor, or patch tags are skip conditions rather than hard failures

### Commands

Run all Helm unit suites:

```bash
helm unittest -f 'tests/units/*_test.yaml' .
```

Run the backward-compatibility script:

```bash
sh tests/units/backward_compatibility_test.sh
```

Notes:

- value file paths inside the unit suites are resolved relative to `tests/units/`
- the backward-compatibility script requires git tags to be available locally

## Smoke Tests

Smoke tests live under `tests/smokes/`.

The structure is intentionally split into small reusable layers:

- `run/` contains the entry point
- `scenarios/` orchestrates complete smoke flows
- `steps/` contains reusable operations
- `fixtures/` contains dedicated smoke-test values files

### Layout

```text
tests/smokes/
├── fixtures/
│   ├── invalid-missing-name.values.yaml
│   └── rendering-contract.values.yaml
├── helpers/
│   └── argparser.py
├── run/
│   └── smoke.py
├── scenarios/
│   └── smoke.py
└── steps/
    ├── chart.py
    ├── crd_schema.py
    ├── helm.py
    ├── kubeconform.py
    ├── render.py
    └── system.py
```

### Scenarios

1. `default-empty`
   Verifies that the chart renders no manifests with default values.

2. `schema-invalid-list-contract`
   Verifies that `values.schema.json` rejects the old list-based top-level resource contract.

3. `schema-invalid-missing-name`
   Verifies that `values.schema.json` rejects a resource item without `name`.

4. `rendering-contract`
   Verifies chart-owned behavior:
   - `nameOverride`
   - merged labels and annotations
   - namespace fallback
   - explicit namespace override
   - global and per-resource `apiVersion`

5. `null-override`
   Verifies that explicit `null` overrides can remove optional example resources without breaking the render.

6. `example-render`
   Renders `values.yaml.example` and verifies that all supported Traefik kinds are produced.

7. `example-kubeconform`
   Renders `values.yaml.example` and validates the result with `kubeconform` against schemas generated from `tests/fixtures/traefik-crd-definition-v1.yml`.

### How kubeconform Works Here

The repository does not depend on an external CRD schema catalog for Traefik resources.

Instead, `tests/smokes/steps/crd_schema.py` extracts the OpenAPI schemas from the vendored Traefik CRD bundle and writes them in the file layout expected by `kubeconform`. CI and local runs use the same mechanism.

### Commands

Run all smoke tests:

```bash
python3 tests/smokes/run/smoke.py
```

Run only one scenario:

```bash
python3 tests/smokes/run/smoke.py --scenario rendering-contract
```

Equivalent `Makefile` targets:

```bash
make test-smoke
make test-smoke-fast
```

## E2E Tests

End-to-end tests live under `tests/e2e/`.

This layer uses a shell runner around `kind` and Helm to validate that the chart can be installed into a real cluster after the Traefik CRDs are registered.

### Layout

```text
tests/e2e/
├── kind.yaml
├── test-e2e.sh
└── values/
    └── install.values.yaml
```

### What the Runner Does

`tests/e2e/test-e2e.sh` performs the following steps:

1. Starts a disposable kind cluster from `tests/e2e/kind.yaml`.
2. Installs the vendored Traefik v3.6 CRD bundle from `tests/fixtures/traefik-crd-definition-v1.yml`.
3. Runs `helm upgrade --install` against the chart root with `tests/e2e/values/install.values.yaml`.
4. Verifies all ten rendered Traefik resources with `kubectl get`.
5. Cleans up the kind cluster on exit.

### Commands

Run the default end-to-end flow:

```bash
bash tests/e2e/test-e2e.sh
```

Pass additional arguments through to `helm upgrade --install`:

```bash
bash tests/e2e/test-e2e.sh --debug
```

Equivalent `Makefile` targets:

```bash
make test-e2e
make test-e2e-debug
make test-e2e-help
```

### Prerequisites

- `kubectl`
- `helm`
- `docker`
- `kind`

Optional environment overrides:

- `CLUSTER_NAME`
- `K8S_VERSION`
- `TRAEFIK_CRD_FILE`

Notes:

- the default `TRAEFIK_CRD_FILE` already points at the vendored upstream bundle
- namespaced resources in `tests/e2e/values/install.values.yaml` rely on the fixed namespace `nuc-traefik-e2e`
- no Traefik controller is installed during e2e; the check is limited to API registration and Helm installability

## Compact Verification

Useful compact commands before opening a change:

```bash
git diff --check
helm lint . -f values.yaml.example
helm template nuc-traefik . -f values.yaml.example
sh -n tests/units/backward_compatibility_test.sh
bash -n tests/e2e/test-e2e.sh
python3 -m py_compile tests/smokes/helpers/argparser.py tests/smokes/run/smoke.py tests/smokes/scenarios/smoke.py tests/smokes/steps/*.py scripts/export-crd-schemas.py
```
