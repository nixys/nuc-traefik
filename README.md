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

Each top-level list in [values.yaml](values.yaml) maps to one Traefik CRD kind:

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

Every list item uses the same generic contract:

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
| ingressRouteTCPs[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRouteTCPs[0].apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRouteTCPs[0].enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRouteTCPs[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRouteTCPs[0].name | string | "" | Resource name. |
| ingressRouteTCPs[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRouteTCPs[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRouteTCPs[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| ingressRouteUDPs[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRouteUDPs[0].apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRouteUDPs[0].enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRouteUDPs[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRouteUDPs[0].name | string | "" | Resource name. |
| ingressRouteUDPs[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRouteUDPs[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRouteUDPs[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| ingressRoutes[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| ingressRoutes[0].apiVersion | string | "" | Per-resource apiVersion override. |
| ingressRoutes[0].enabled | bool | `false` | Enable rendering of this resource item. |
| ingressRoutes[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| ingressRoutes[0].name | string | "" | Resource name. |
| ingressRoutes[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| ingressRoutes[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| ingressRoutes[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| middlewareTCPs[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| middlewareTCPs[0].apiVersion | string | "" | Per-resource apiVersion override. |
| middlewareTCPs[0].enabled | bool | `false` | Enable rendering of this resource item. |
| middlewareTCPs[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| middlewareTCPs[0].name | string | "" | Resource name. |
| middlewareTCPs[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| middlewareTCPs[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| middlewareTCPs[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| middlewares[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| middlewares[0].apiVersion | string | "" | Per-resource apiVersion override. |
| middlewares[0].enabled | bool | `false` | Enable rendering of this resource item. |
| middlewares[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| middlewares[0].name | string | "" | Resource name. |
| middlewares[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| middlewares[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| middlewares[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| nameOverride | string | `""` | Override the default chart label name if needed. |
| serversTransportTCPs[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| serversTransportTCPs[0].apiVersion | string | "" | Per-resource apiVersion override. |
| serversTransportTCPs[0].enabled | bool | `false` | Enable rendering of this resource item. |
| serversTransportTCPs[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| serversTransportTCPs[0].name | string | "" | Resource name. |
| serversTransportTCPs[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| serversTransportTCPs[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| serversTransportTCPs[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| serversTransports[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| serversTransports[0].apiVersion | string | "" | Per-resource apiVersion override. |
| serversTransports[0].enabled | bool | `false` | Enable rendering of this resource item. |
| serversTransports[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| serversTransports[0].name | string | "" | Resource name. |
| serversTransports[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| serversTransports[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| serversTransports[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| tlsOptions[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| tlsOptions[0].apiVersion | string | "" | Per-resource apiVersion override. |
| tlsOptions[0].enabled | bool | `false` | Enable rendering of this resource item. |
| tlsOptions[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| tlsOptions[0].name | string | "" | Resource name. |
| tlsOptions[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| tlsOptions[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| tlsOptions[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| tlsStores[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| tlsStores[0].apiVersion | string | "" | Per-resource apiVersion override. |
| tlsStores[0].enabled | bool | `false` | Enable rendering of this resource item. |
| tlsStores[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| tlsStores[0].name | string | "" | Resource name. |
| tlsStores[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| tlsStores[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| tlsStores[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |
| traefikServices[0].annotations | object | {} | Resource-specific annotations merged on top of commonAnnotations. |
| traefikServices[0].apiVersion | string | "" | Per-resource apiVersion override. |
| traefikServices[0].enabled | bool | `false` | Enable rendering of this resource item. |
| traefikServices[0].labels | object | {} | Resource-specific labels merged on top of built-in chart labels and commonLabels. |
| traefikServices[0].name | string | "" | Resource name. |
| traefikServices[0].namespace | string | "" | Resource namespace. Defaults to the Helm release namespace when empty. |
| traefikServices[0].spec | object | {} | Arbitrary resource spec rendered as-is. |
| traefikServices[0].status | object | {} | Optional resource status rendered as-is for fixtures and synthetic manifests. |

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
