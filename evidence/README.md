# Evidence index

Captured from the actual local stack and GitHub Actions on 16 October 2026.

| Evidence | Description |
|---|---|
| `01-compose-browser.jpg` | Browser workflow on the Compose stack |
| `02-kubernetes-ingress.jpg` | Application accessed through Kubernetes Ingress |
| `03-grafana-dashboard.jpg` | Live application metrics in Grafana |
| `04-mobile-browser.jpg` | Mobile viewport screenshot |
| `05-prometheus-targets.jpg` | Backend scrape pool UP |
| `06-actions-success.jpg` | Public GitHub Actions success page |
| `07-pytest-output.jpg` through `11-frontend-scan.jpg` | Screenshots of the raw-output browser viewer, clearly labelled |
| `12-commit-history.jpg` | Public GitHub commit history, only praneethb7 |
| `13-ghcr-backend.jpg`, `14-ghcr-frontend.jpg` | Public SHA-tagged GHCR package pages |
| `registry-backend.json`, `registry-frontend.json` | Anonymous pull verification and content digests |
| `deployed-release.txt`, `local-rollout.txt` | Exact-source local Helm rollout and API revision verification |
| `15-metrics-output.jpg`, `16-helm-output.jpg`, `17-deployed-release.jpg` | Actual metrics, Helm release and verified API source revision in the labelled output viewer |
| `pytest.txt` | 18-test run against isolated PostgreSQL and coverage |
| `compose.txt` | Actual healthy Compose services |
| `kubernetes.txt`, `helm.txt` | Workloads, Services, Ingress, HPA and Helm release |
| `database.txt` | Actual PostgreSQL tables, migration revision and inventory |
| `metrics.txt` | Actual Prometheus exposition output |
| `hpa-scale-up.txt`, `hpa-events.txt` | Two-to-five autoscaling result and event |
| `service-before.txt`, `service-after.txt` | Service selector failure and populated endpoints after repair |
| `broken-image.txt` | Missing image tag diagnosis |
| `terraform-validate.txt`, `terraform-mock-tests.txt` | HCL validation and mock-only planning tests |
| `security-backend/`, `security-frontend/` | Original Trivy artifacts from successful CI |
| `pipeline.json` | Successful run and job metadata |
| `commits.txt` | Meaningful capstone commit history and attribution |

Text captures are not screenshots of a terminal. AWS provisioning, AWS Console and destroy evidence do not exist because AWS provisioning was not authorized. See `docs/SUBMISSION.md` for outstanding presentation/form steps.
