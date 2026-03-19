#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.smokes.steps.crd_schema import (  # noqa: E402
    export_kubeconform_schemas,
    schema_location_template,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export kubeconform schemas from a vendored Kubernetes CRD bundle."
    )
    parser.add_argument(
        "--crd-file",
        required=True,
        help="Path to the CRD YAML bundle.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where kubeconform schema files should be written.",
    )
    parser.add_argument(
        "--print-template",
        action="store_true",
        help="Print the resulting kubeconform schema location template.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output_dir = export_kubeconform_schemas(
        crd_bundle=Path(args.crd_file).resolve(),
        output_dir=Path(args.output_dir).resolve(),
    )
    if args.print_template:
        print(schema_location_template(output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
