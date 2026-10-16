#!/usr/bin/env bash
# Build this checkout at its exact source revision and deploy to local Minikube.
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"
git diff --quiet -- backend frontend helm || { echo 'Commit application/chart changes before tagging a deployment.' >&2; exit 1; }
source_sha="$(git rev-parse HEAD)"
monitoring_enabled="${MONITORING_ENABLED:-false}"
case "$monitoring_enabled" in true|false) ;; *) echo 'MONITORING_ENABLED must be true or false.' >&2; exit 1 ;; esac
minikube status >/dev/null 2>&1 || minikube start --driver=docker
minikube addons enable ingress
minikube addons enable metrics-server
docker build --label "org.opencontainers.image.revision=$source_sha" -t "campuscrate-backend:$source_sha" ./backend
docker build --label "org.opencontainers.image.revision=$source_sha" -t "campuscrate-frontend:$source_sha" ./frontend
minikube image load "campuscrate-backend:$source_sha" "campuscrate-frontend:$source_sha"
bash scripts/bootstrap-secret.sh
helm upgrade --install campuscrate helm/campuscrate -n campuscrate \
  --set backend.image=campuscrate-backend --set "backend.tag=$source_sha" \
  --set frontend.image=campuscrate-frontend --set "frontend.tag=$source_sha" \
  --set "monitoring.enabled=$monitoring_enabled" --wait --wait-for-jobs --timeout 5m
kubectl -n campuscrate rollout status deployment/backend --timeout=120s
kubectl -n campuscrate rollout status deployment/frontend --timeout=120s
kubectl -n campuscrate exec deployment/backend -- python -c \
  "import json,urllib.request; data=json.load(urllib.request.urlopen('http://localhost:8000/')); assert data['release']=='$source_sha',data; print(json.dumps(data))"
printf 'Verified local rollout of source revision %s\n' "$source_sha"
