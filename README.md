# NUC Traefik

Helm chart for rendering Traefik Kubernetes CRD resources from declarative values.

The chart does not install Traefik CRDs or the Traefik controller. It only renders Traefik CRD objects that are already supported by the target cluster.

Defaults are aligned with the Traefik v3.6 CRD bundle published at [raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml](https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml). The exact bundle is vendored under `tests/fixtures/` and reused by smoke validation and local e2e.

## Quick Start

Render the example configuration:

```bash
helm template nuc-traefik . -f values.yaml.example
```

Install the chart:

```bash
helm install nuc-traefik . \
  --namespace traefik-system \
  --create-namespace \
  -f values.yaml.example
```

Install the local README generator hook:

```bash
pre-commit install
pre-commit install-hooks
```

## Supported Resources

The chart can render these Traefik CRD kinds:

- `IngressRoute`
- `IngressRouteTCP`
- `IngressRouteUDP`
- `Middleware`
- `MiddlewareTCP`
- `ServersTransport`
- `ServersTransportTCP`
- `TLSOption`
- `TLSStore`
- `TraefikService`

## Values Model

Each top-level map in [values.yaml](values.yaml) maps to one Traefik CRD kind:

- `ingressRoutes`
- `ingressRouteTCPs`
- `ingressRouteUDPs`
- `middlewares`
- `middlewareTCPs`
- `serversTransports`
- `serversTransportTCPs`
- `tlsOptions`
- `tlsStores`
- `traefikServices`

Every map entry uses the same generic contract:

| Field | Required | Description |
|-------|----------|-------------|
| `enabled` | no | When `false`, the chart skips rendering the item. |
| `name` | yes | Resource name. |
| `namespace` | no | Namespace for namespaced resources. Defaults to the Helm release namespace. |
| `labels` | no | Labels merged on top of built-in chart labels and `commonLabels`. |
| `annotations` | no | Annotations merged on top of `commonAnnotations`. |
| `apiVersion` | no | Per-resource API version override. |
| `spec` | no | Raw resource spec rendered as-is. |
| `status` | no | Optional raw status block. Usually useful only for fixtures and synthetic manifests. |

The map key is only an identifier inside `values.yaml`; the rendered Kubernetes object name still comes from the required `name` field.

Global controls:

- `nameOverride`
- `commonLabels`
- `commonAnnotations`
- `apiVersions.*`

The value contract is validated by [values.schema.json](values.schema.json).

## Helm Values

This section is generated from [values.yaml](values.yaml) by `helm-docs`. Edit [values.yaml](values.yaml) comments or [docs/README.md.gotmpl](docs/README.md.gotmpl), then run `pre-commit run helm-docs --all-files` or `make docs`.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| apiVersions.ingressRoute | string | `"traefik.io/v1alpha1"` | Default apiVersion for IngressRoute resources. |
| apiVersions.ingressRouteTCP | string | `"traefik.io/v1alpha1"` | Default apiVersion for IngressRouteTCP resources. |
| apiVersions.ingressRouteUDP | string | `"traefik.io/v1alpha1"` | Default apiVersion for IngressRouteUDP resources. |
| apiVersions.middleware | string | `"traefik.io/v1alpha1"` | Default apiVersion for Middleware resources. |
| apiVersions.middlewareTCP | string | `"traefik.io/v1alpha1"` | Default apiVersion for MiddlewareTCP resources. |
| apiVersions.serversTransport | string | `"traefik.io/v1alpha1"` | Default apiVersion for ServersTransport resources. |
| apiVersions.serversTransportTCP | string | `"traefik.io/v1alpha1"` | Default apiVersion for ServersTransportTCP resources. |
| apiVersions.tlsOption | string | `"traefik.io/v1alpha1"` | Default apiVersion for TLSOption resources. |
| apiVersions.tlsStore | string | `"traefik.io/v1alpha1"` | Default apiVersion for TLSStore resources. |
| apiVersions.traefikService | string | `"traefik.io/v1alpha1"` | Default apiVersion for TraefikService resources. |
| commonAnnotations | object | `{}` | Extra annotations applied to every rendered resource. |
| commonLabels | object | `{}` | Extra labels applied to every rendered resource. |
| ingressRouteTCPs.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRouteTCPs.example.apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRouteTCPs.example.enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRouteTCPs.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRouteTCPs.example.name | string | "" | Resource name. |
| ingressRouteTCPs.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRouteTCPs.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRouteTCPs.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| ingressRouteUDPs.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRouteUDPs.example.apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRouteUDPs.example.enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRouteUDPs.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRouteUDPs.example.name | string | "" | Resource name. |
| ingressRouteUDPs.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRouteUDPs.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRouteUDPs.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| ingressRoutes.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRoutes.example.apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRoutes.example.enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRoutes.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRoutes.example.name | string | "" | Resource name. |
| ingressRoutes.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRoutes.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRoutes.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| middlewareTCPs.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| middlewareTCPs.example.apiVersion | string | "" | Per-resource apiVersion override. |
| middlewareTCPs.example.enabled | bool | `false` | Enable rendering of this resource item. |
| middlewareTCPs.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| middlewareTCPs.example.name | string | "" | Resource name. |
| middlewareTCPs.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| middlewareTCPs.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| middlewareTCPs.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| middlewares.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| middlewares.example.apiVersion | string | "" | Per-resource apiVersion override. |
| middlewares.example.enabled | bool | `false` | Enable rendering of this resource item. |
| middlewares.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| middlewares.example.name | string | "" | Resource name. |
| middlewares.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| middlewares.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| middlewares.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| nameOverride | string | `""` | Override the default chart label name if needed. |
| serversTransportTCPs.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| serversTransportTCPs.example.apiVersion | string | "" | Per-resource apiVersion override. |
| serversTransportTCPs.example.enabled | bool | `false` | Enable rendering of this resource item. |
| serversTransportTCPs.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| serversTransportTCPs.example.name | string | "" | Resource name. |
| serversTransportTCPs.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| serversTransportTCPs.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| serversTransportTCPs.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| serversTransports.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| serversTransports.example.apiVersion | string | "" | Per-resource apiVersion override. |
| serversTransports.example.enabled | bool | `false` | Enable rendering of this resource item. |
| serversTransports.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| serversTransports.example.name | string | "" | Resource name. |
| serversTransports.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| serversTransports.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| serversTransports.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| tlsOptions.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| tlsOptions.example.apiVersion | string | "" | Per-resource apiVersion override. |
| tlsOptions.example.enabled | bool | `false` | Enable rendering of this resource item. |
| tlsOptions.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| tlsOptions.example.name | string | "" | Resource name. |
| tlsOptions.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| tlsOptions.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| tlsOptions.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| tlsStores.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| tlsStores.example.apiVersion | string | "" | Per-resource apiVersion override. |
| tlsStores.example.enabled | bool | `false` | Enable rendering of this resource item. |
| tlsStores.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| tlsStores.example.name | string | "" | Resource name. |
| tlsStores.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| tlsStores.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| tlsStores.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| traefikServices.example.annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| traefikServices.example.apiVersion | string | "" | Per-resource apiVersion override. |
| traefikServices.example.enabled | bool | `false` | Enable rendering of this resource item. |
| traefikServices.example.labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| traefikServices.example.name | string | "" | Resource name. |
| traefikServices.example.namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| traefikServices.example.spec | object | {} | Arbitrary resource spec rendered as-is. |
| traefikServices.example.status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |

## Included Values Files

- [values.yaml](values.yaml): minimal defaults that render no resources.
- [values.yaml.example](values.yaml.example): complete example covering every supported resource kind.

## Testing

The repository uses three test layers:

- `tests/units/` for `helm-unittest` suites and backward compatibility checks
- `tests/smokes/` for render and schema smoke scenarios
- `tests/e2e/` for local kind-based Helm install checks against the vendored Traefik CRDs

Representative local commands:

```bash
helm lint . -f values.yaml.example
helm template nuc-traefik . -f values.yaml.example
helm unittest -f 'tests/units/*_test.yaml' .
sh tests/units/backward_compatibility_test.sh
python3 tests/smokes/run/smoke.py --scenario example-render
make test-e2e
```

Detailed test documentation is available in [docs/TESTS.MD](docs/TESTS.MD). Local setup instructions are in [docs/DEPENDENCY.md](docs/DEPENDENCY.md).

## Notes

- All supported resources in the pinned Traefik v3.6 bundle are namespaced.
- `apiVersions.*` stays part of the public contract so the chart can render against clusters with another served group/version.
- [tests/fixtures/traefik-crd-definition-v1.yml](tests/fixtures/traefik-crd-definition-v1.yml) is the single source used for e2e CRD bootstrap and `kubeconform` schema export.

## Repository Layout

| Path | Purpose |
|------|---------|
| [Chart.yaml](Chart.yaml) | Chart metadata. |
| [values.yaml](values.yaml) | Minimal default values and `helm-docs` source comments. |
| [docs/README.md.gotmpl](docs/README.md.gotmpl) | Template used by `helm-docs` to build `README.md`. |
| [values.yaml.example](values.yaml.example) | Full example configuration. |
| [values.schema.json](values.schema.json) | JSON schema for chart values. |
| [templates/](templates) | One template per supported Traefik CRD kind plus shared helpers. |
| [tests/fixtures/traefik-crd-definition-v1.yml](tests/fixtures/traefik-crd-definition-v1.yml) | Vendored upstream CRD bundle from Traefik v3.6. |
| [tests/units/](tests/units) | Helm unit suites and backward compatibility checks. |
| [tests/smokes/](tests/smokes) | Smoke scenarios for render and schema validation. |
| [tests/e2e/](tests/e2e) | kind-based end-to-end installation checks. |
| [docs/DEPENDENCY.md](docs/DEPENDENCY.md) | Local dependency installation guide for development and tests. |
| [docs/TESTS.MD](docs/TESTS.MD) | Detailed testing documentation. |
