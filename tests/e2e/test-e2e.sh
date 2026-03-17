#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
SCRIPT_DIR="${ROOT_DIR}/tests/e2e"
CLUSTER_CREATED=false
CLUSTER_NAME="${CLUSTER_NAME:-$(mktemp -u "nuc-traefik-e2e-XXXXXXXXXX" | tr "[:upper:]" "[:lower:]")}"
# kindest/node images are published on kind's cadence, not for every Kubernetes patch release.
K8S_VERSION="${K8S_VERSION:-v1.35.0}"
TRAEFIK_CRD_FILE="${TRAEFIK_CRD_FILE:-${ROOT_DIR}/tests/fixtures/traefik-crd-definition-v1.yml}"
TRAEFIK_CRD_SOURCE_URL="https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml"
E2E_NAMESPACE="nuc-traefik-e2e"
RELEASE_NAME="nuc-traefik-e2e"
VALUES_FILE="tests/e2e/values/install.values.yaml"

RED='\033[0;31m'
YELLOW='\033[0;33m'
RESET='\033[0m'

log_error() { echo -e "${RED}Error:${RESET} $1" >&2; }
log_info() { echo -e "$1"; }
log_warn() { echo -e "${YELLOW}Warning:${RESET} $1" >&2; }

show_help() {
  echo "Usage: $(basename "$0") [helm upgrade/install options]"
  echo ""
  echo "Create a kind cluster, install the vendored Traefik v3.6 CRDs, and run Helm install/upgrade against the root chart."
  echo "Unknown arguments are passed through to 'helm upgrade --install'."
  echo ""
  echo "Environment overrides:"
  echo "  CLUSTER_NAME       Kind cluster name"
  echo "  K8S_VERSION        kindest/node tag"
  echo "  TRAEFIK_CRD_FILE   Local path to the Traefik CRD bundle"
  echo ""
  echo "Vendored CRD source:"
  echo "  ${TRAEFIK_CRD_SOURCE_URL}"
  echo ""
}

verify_prerequisites() {
  for bin in docker kind kubectl helm; do
    if ! command -v "${bin}" >/dev/null 2>&1; then
      log_error "${bin} is not installed"
      exit 1
    fi
  done

  if [ ! -f "${TRAEFIK_CRD_FILE}" ]; then
    log_error "Traefik CRD bundle not found at ${TRAEFIK_CRD_FILE}"
    exit 1
  fi
}

cleanup() {
  local exit_code=$?

  if [ "${exit_code}" -ne 0 ] && [ "${CLUSTER_CREATED}" = true ]; then
    dump_cluster_state || true
  fi

  log_info "Cleaning up resources"

  if [ "${CLUSTER_CREATED}" = true ]; then
    log_info "Removing kind cluster ${CLUSTER_NAME}"
    if kind get clusters | grep -q "${CLUSTER_NAME}"; then
      kind delete cluster --name="${CLUSTER_NAME}"
    else
      log_warn "kind cluster ${CLUSTER_NAME} not found"
    fi
  fi

  exit "${exit_code}"
}

dump_cluster_state() {
  log_warn "Dumping Traefik CRD resources from ${CLUSTER_NAME}"
  kubectl -n "${E2E_NAMESPACE}" get \
    ingressroutes.traefik.io,ingressroutetcps.traefik.io,ingressrouteudps.traefik.io,middlewares.traefik.io,middlewaretcps.traefik.io,serverstransports.traefik.io,serverstransporttcps.traefik.io,tlsoptions.traefik.io,tlsstores.traefik.io,traefikservices.traefik.io \
    || true
}

create_kind_cluster() {
  log_info "Creating kind cluster ${CLUSTER_NAME}"

  if kind get clusters | grep -q "${CLUSTER_NAME}"; then
    log_error "kind cluster ${CLUSTER_NAME} already exists"
    exit 1
  fi

  kind create cluster \
    --name="${CLUSTER_NAME}" \
    --config="${SCRIPT_DIR}/kind.yaml" \
    --image="kindest/node:${K8S_VERSION}" \
    --wait=60s

  CLUSTER_CREATED=true
  echo
}

install_traefik_crds() {
  log_info "Installing Traefik CRDs from ${TRAEFIK_CRD_FILE}"
  kubectl apply --server-side -f "${TRAEFIK_CRD_FILE}"

  for crd in \
    ingressroutes.traefik.io \
    ingressroutetcps.traefik.io \
    ingressrouteudps.traefik.io \
    middlewares.traefik.io \
    middlewaretcps.traefik.io \
    serverstransports.traefik.io \
    serverstransporttcps.traefik.io \
    tlsoptions.traefik.io \
    tlsstores.traefik.io \
    traefikservices.traefik.io; do
    kubectl wait --for=condition=Established --timeout=120s "crd/${crd}"
  done

  echo
}

ensure_namespace() {
  log_info "Ensuring namespace ${E2E_NAMESPACE} exists"
  kubectl get namespace "${E2E_NAMESPACE}" >/dev/null 2>&1 || kubectl create namespace "${E2E_NAMESPACE}"
  echo
}

install_chart() {
  local helm_args=(
    upgrade
    --install
    "${RELEASE_NAME}"
    "${ROOT_DIR}"
    --namespace "${E2E_NAMESPACE}"
    -f "${ROOT_DIR}/${VALUES_FILE}"
    --wait
    --timeout 300s
  )

  if [ "$#" -gt 0 ]; then
    helm_args+=("$@")
  fi

  log_info "Building chart dependencies"
  helm dependency build "${ROOT_DIR}"
  echo

  log_info "Installing chart with Helm"
  helm "${helm_args[@]}"
  echo
}

verify_release_resources() {
  log_info "Verifying installed Traefik CRD resources"
  kubectl -n "${E2E_NAMESPACE}" get ingressroutes.traefik.io e2e-http
  kubectl -n "${E2E_NAMESPACE}" get ingressroutetcps.traefik.io e2e-tcp
  kubectl -n "${E2E_NAMESPACE}" get ingressrouteudps.traefik.io e2e-udp
  kubectl -n "${E2E_NAMESPACE}" get middlewares.traefik.io e2e-api-security
  kubectl -n "${E2E_NAMESPACE}" get middlewaretcps.traefik.io e2e-db-allowlist
  kubectl -n "${E2E_NAMESPACE}" get serverstransports.traefik.io e2e-http-transport
  kubectl -n "${E2E_NAMESPACE}" get serverstransporttcps.traefik.io e2e-tcp-transport
  kubectl -n "${E2E_NAMESPACE}" get tlsoptions.traefik.io e2e-modern-tls
  kubectl -n "${E2E_NAMESPACE}" get tlsstores.traefik.io default
  kubectl -n "${E2E_NAMESPACE}" get traefikservices.traefik.io e2e-weighted
  echo
}

parse_args() {
  for arg in "$@"; do
    case "${arg}" in
      -h|--help)
        show_help
        exit 0
        ;;
    esac
  done
}

main() {
  parse_args "$@"
  verify_prerequisites

  trap cleanup EXIT

  create_kind_cluster
  install_traefik_crds
  ensure_namespace
  install_chart "$@"
  verify_release_resources

  log_info "End-to-end checks completed successfully"
}

main "$@"
