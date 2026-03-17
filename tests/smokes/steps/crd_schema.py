from __future__ import annotations

import json
from pathlib import Path

import yaml

from tests.smokes.steps.system import TestFailure


def export_kubeconform_schemas(*, crd_bundle: Path, output_dir: Path) -> Path:
    if not crd_bundle.exists():
        raise TestFailure(f"CRD bundle not found: {crd_bundle}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with crd_bundle.open("r", encoding="utf-8") as handle:
        documents = list(yaml.safe_load_all(handle))

    exported = 0
    for document in documents:
        if not document or document.get("kind") != "CustomResourceDefinition":
            continue

        spec = document.get("spec", {})
        group = spec.get("group")
        kind = spec.get("names", {}).get("kind")
        if not group or not kind:
            continue

        for version in spec.get("versions", []):
            schema = version.get("schema", {}).get("openAPIV3Schema")
            version_name = version.get("name")
            if not schema or not version_name:
                continue

            payload = dict(schema)
            payload.setdefault("$schema", "https://json-schema.org/draft-07/schema#")

            filenames = {
                f"{kind}_{version_name}.json",
                f"{kind.lower()}_{version_name}.json",
            }
            for filename in filenames:
                destination = output_dir / group / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(
                    json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                exported += 1

    if exported == 0:
        raise TestFailure(f"no schemas exported from CRD bundle: {crd_bundle}")

    return output_dir


def schema_location_template(schema_root: Path) -> str:
    return str(schema_root / "{{.Group}}" / "{{.ResourceKind}}_{{.ResourceAPIVersion}}.json")
