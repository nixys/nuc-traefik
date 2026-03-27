from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from tests.smokes.steps import chart, crd_schema, helm, kubeconform, render, system


@dataclass
class SmokeContext:
    repo_root: Path
    workdir: Path
    chart_dir: Path
    render_dir: Path
    release_name: str
    namespace: str
    kube_version: str
    kubeconform_bin: str
    schema_location: str
    skip_kinds: str

    @property
    def crd_bundle(self) -> Path:
        return self.repo_root / "tests" / "fixtures" / "traefik-crd-definition-v1.yml"

    @property
    def example_values(self) -> Path:
        return self.repo_root / "values.yaml.example"

    @property
    def rendering_contract_values(self) -> Path:
        return (
            self.repo_root
            / "tests"
            / "smokes"
            / "fixtures"
            / "rendering-contract.values.yaml"
        )

    @property
    def invalid_missing_name_values(self) -> Path:
        return (
            self.repo_root
            / "tests"
            / "smokes"
            / "fixtures"
            / "invalid-missing-name.values.yaml"
        )

    @property
    def invalid_list_contract_values(self) -> Path:
        return (
            self.repo_root
            / "tests"
            / "smokes"
            / "fixtures"
            / "invalid-list-contract.values.yaml"
        )

    @property
    def null_override_values(self) -> Path:
        return (
            self.repo_root
            / "tests"
            / "smokes"
            / "fixtures"
            / "null-override.values.yaml"
        )


def check_default_empty(context: SmokeContext) -> None:
    helm.lint(context.chart_dir, workdir=context.workdir)
    output_path = context.render_dir / "default-empty.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        output_path=output_path,
        workdir=context.workdir,
    )
    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 0)


def check_schema_invalid_missing_name(context: SmokeContext) -> None:
    result = helm.lint(
        context.chart_dir,
        values_file=context.invalid_missing_name_values,
        workdir=context.workdir,
        check=False,
    )
    if result.returncode == 0:
        raise system.TestFailure(
            "helm lint unexpectedly succeeded for invalid values without resource name"
        )

    combined_output = f"{result.stdout}\n{result.stderr}"
    if "name" not in combined_output:
        raise system.TestFailure(
            "helm lint failed for invalid values, but the error does not mention the missing name field"
        )


def check_schema_invalid_list_contract(context: SmokeContext) -> None:
    result = helm.lint(
        context.chart_dir,
        values_file=context.invalid_list_contract_values,
        workdir=context.workdir,
        check=False,
    )
    if result.returncode == 0:
        raise system.TestFailure(
            "helm lint unexpectedly succeeded for invalid list-based resource values"
        )

    combined_output = f"{result.stdout}\n{result.stderr}".lower()
    if "ingressroutes" not in combined_output or "array" not in combined_output:
        raise system.TestFailure(
            "helm lint failed for invalid list-based values, but the error does not mention the array/object contract"
        )


def check_rendering_contract(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.rendering_contract_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "rendering-contract.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.rendering_contract_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 2)

    ingress_route = render.select_document(
        documents, kind="IngressRoute", name="merged-ingressroute"
    )
    render.assert_path(ingress_route, "apiVersion", "example.net/v1alpha1")
    render.assert_path(ingress_route, "metadata.namespace", context.namespace)
    render.assert_path(
        ingress_route,
        "metadata.labels[app.kubernetes.io/name]",
        "traefik-platform",
    )
    render.assert_path(ingress_route, "metadata.labels.platform", "traefik-crd")
    render.assert_path(ingress_route, "metadata.labels.component", "ingress-route")
    render.assert_path(ingress_route, "metadata.labels.tier", "edge")
    render.assert_path(ingress_route, "metadata.annotations.team", "platform")
    render.assert_path(ingress_route, "metadata.annotations.note", "external")
    render.assert_path(ingress_route, "spec.routes[0].services[0].port", 8080)

    tls_store = render.select_document(documents, kind="TLSStore", name="tenant-store")
    render.assert_path(tls_store, "apiVersion", "example.net/v1beta1")
    render.assert_path(tls_store, "metadata.namespace", "tenant-system")
    render.assert_path(
        tls_store,
        "metadata.labels[app.kubernetes.io/name]",
        "traefik-platform",
    )
    render.assert_path(tls_store, "metadata.labels.component", "tls-store")
    render.assert_path(tls_store, "metadata.annotations.team", "platform")
    render.assert_path(tls_store, "metadata.annotations.note", "tenant")
    render.assert_path(
        tls_store, "spec.defaultCertificate.secretName", "tenant-cert"
    )


def check_null_override(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.example_values,
        values_files=[context.null_override_values],
        workdir=context.workdir,
    )
    output_path = context.render_dir / "null-override.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        values_files=[context.null_override_values],
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 9)
    render.assert_kinds(
        documents,
        {
            "IngressRoute",
            "IngressRouteTCP",
            "IngressRouteUDP",
            "MiddlewareTCP",
            "ServersTransport",
            "ServersTransportTCP",
            "TLSOption",
            "TLSStore",
            "TraefikService",
        },
    )

    tls_store = render.select_document(documents, kind="TLSStore", name="default")
    render.assert_path(tls_store, "metadata.namespace", "edge")


def check_example_render(context: SmokeContext) -> None:
    helm.lint(
        context.chart_dir,
        values_file=context.example_values,
        workdir=context.workdir,
    )
    output_path = context.render_dir / "example-render.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )

    documents = render.load_documents(output_path)
    render.assert_doc_count(documents, 10)
    render.assert_kinds(
        documents,
        {
            "IngressRoute",
            "IngressRouteTCP",
            "IngressRouteUDP",
            "Middleware",
            "MiddlewareTCP",
            "ServersTransport",
            "ServersTransportTCP",
            "TLSOption",
            "TLSStore",
            "TraefikService",
        },
    )

    ingress_route = render.select_document(documents, kind="IngressRoute", name="api-http")
    render.assert_path(ingress_route, "metadata.namespace", "edge")
    render.assert_path(ingress_route, "spec.routes[0].services[0].kind", "TraefikService")

    ingress_route_tcp = render.select_document(
        documents, kind="IngressRouteTCP", name="postgres-tcp"
    )
    render.assert_path(ingress_route_tcp, "spec.tls.options.name", "modern-tls")

    ingress_route_udp = render.select_document(
        documents, kind="IngressRouteUDP", name="dns-udp"
    )
    render.assert_path(ingress_route_udp, "spec.routes[0].services[1].weight", 5)

    middleware = render.select_document(documents, kind="Middleware", name="api-security")
    render.assert_path(
        middleware, "spec.headers.customRequestHeaders.X-Forwarded-Env", "production"
    )

    middleware_tcp = render.select_document(
        documents, kind="MiddlewareTCP", name="db-allowlist"
    )
    render.assert_path(middleware_tcp, "spec.ipAllowList.sourceRange[0]", "10.0.0.0/8")

    servers_transport = render.select_document(
        documents, kind="ServersTransport", name="backend-transport"
    )
    render.assert_path(
        servers_transport, "spec.forwardingTimeouts.responseHeaderTimeout", "15s"
    )

    servers_transport_tcp = render.select_document(
        documents, kind="ServersTransportTCP", name="database-transport"
    )
    render.assert_path(
        servers_transport_tcp, "spec.tls.serverName", "db.internal.example.com"
    )

    tls_option = render.select_document(documents, kind="TLSOption", name="modern-tls")
    render.assert_path(tls_option, "spec.clientAuth.secretNames[0]", "edge-client-ca")

    tls_store = render.select_document(documents, kind="TLSStore", name="default")
    render.assert_path(tls_store, "spec.defaultCertificate.secretName", "edge-default-cert")

    traefik_service = render.select_document(
        documents, kind="TraefikService", name="api-weighted"
    )
    render.assert_path(traefik_service, "spec.weighted.services[1].weight", 10)


def check_example_kubeconform(context: SmokeContext) -> None:
    output_path = context.render_dir / "example-kubeconform.yaml"
    helm.template(
        context.chart_dir,
        release_name=context.release_name,
        namespace=context.namespace,
        values_file=context.example_values,
        output_path=output_path,
        workdir=context.workdir,
    )
    kubeconform.validate(
        manifest_path=output_path,
        kube_version=context.kube_version,
        kubeconform_bin=context.kubeconform_bin,
        schema_location=context.schema_location,
        skip_kinds=context.skip_kinds,
    )


SCENARIOS: list[tuple[str, Callable[[SmokeContext], None]]] = [
    ("default-empty", check_default_empty),
    ("schema-invalid-list-contract", check_schema_invalid_list_contract),
    ("schema-invalid-missing-name", check_schema_invalid_missing_name),
    ("rendering-contract", check_rendering_contract),
    ("null-override", check_null_override),
    ("example-render", check_example_render),
    ("example-kubeconform", check_example_kubeconform),
]


def run_smoke_suite(args) -> int:
    scenario_map = dict(SCENARIOS)
    requested = args.scenario or ["all"]
    if "all" in requested:
        selected = [name for name, _ in SCENARIOS]
    else:
        selected = requested

    repo_root = Path(args.chart_dir).resolve()
    workdir, chart_dir = chart.stage_chart(repo_root, args.workdir)
    schema_location = args.schema_location
    schema_root = None
    if schema_location:
        schema_root = crd_schema.resolve_local_schema_root(
            schema_location,
            base_dir=repo_root,
        )
    else:
        schema_root = workdir / "schemas"

    if schema_root is not None:
        crd_schema.export_kubeconform_schemas(
            crd_bundle=repo_root / "tests" / "fixtures" / "traefik-crd-definition-v1.yml",
            output_dir=schema_root,
        )
    if not schema_location:
        schema_location = crd_schema.schema_location_template(schema_root)

    context = SmokeContext(
        repo_root=repo_root,
        workdir=workdir,
        chart_dir=chart_dir,
        render_dir=workdir / "rendered",
        release_name=args.release_name,
        namespace=args.namespace,
        kube_version=args.kube_version,
        kubeconform_bin=args.kubeconform_bin,
        schema_location=schema_location,
        skip_kinds=args.skip_kinds,
    )
    context.render_dir.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[str, str]] = []
    try:
        for name in selected:
            system.log(f"=== scenario: {name} ===")
            try:
                scenario_map[name](context)
            except Exception as exc:
                failures.append((name, str(exc)))
                system.log(f"FAILED: {name}: {exc}")
            else:
                system.log(f"PASSED: {name}")
    finally:
        if args.keep_workdir:
            system.log(f"workdir kept at {workdir}")
        else:
            chart.cleanup(workdir)

    if failures:
        system.log("=== summary: failures ===")
        for name, message in failures:
            system.log(f"- {name}: {message}")
        return 1

    system.log("=== summary: all smoke scenarios passed ===")
    return 0
