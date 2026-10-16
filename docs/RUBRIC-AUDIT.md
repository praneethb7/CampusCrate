# Instructor requirements audit

Checked against the instructor's [README](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/README.md) and [grading rubric](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/GRADING.md) on 16 October 2026. The referenced student guide was not present in that directory.

## Technical coverage

| Requirement | Implementation | Verification |
|---|---|---|
| Original application domain | Campus equipment inventory and loans; original interface and business rules | Browser create/borrow/return workflow |
| React frontend and responsive UI | `frontend/src/` | Production build and desktop/mobile browser captures |
| FastAPI health and REST CRUD | `backend/app/` | 18 PostgreSQL tests, deployed smoke test; GET/POST/PUT/DELETE |
| PostgreSQL with Alembic | Equipment and loan ledger; initial migration and indexed foreign key | Direct SQL capture; CI migration round-trip and schema-drift check |
| Isolated tests, minimum five | 18 tests; disposable test databases; `_test` database-name guard | Includes simultaneous allocation and duplicate-return races |
| Git, public repository, 10+ meaningful commits | Standalone CampusCrate repository with project history under praneethb7 | Commit history and public access |
| Ignore local credentials/dependencies | Root `.gitignore`, per-image `.dockerignore` | Local `.env`, virtualenv, node_modules and Terraform state excluded |
| Backend Dockerfile and multi-stage frontend | Python build/runtime stages; Node build to unprivileged Nginx | Both images build and non-root UIDs verified |
| One-command three-tier stack | Compose plus gated migration task | Healthy frontend/backend/database and successful migration |
| Every main push runs CI | Root workflow has no push-path filter | New standalone repository pipeline |
| Tests/build before publication | Test → parallel builds/scans → publish → deploy | GitHub Actions dependency graph |
| GHCR SHA image tags | `campuscrate-api:<SHA>` and `campuscrate-web:<SHA>` | Public package pages; anonymous registry digest receipts |
| Trivy both images; fail HIGH/CRITICAL | Unfixed findings remain included; no allowlist | Original reports and remediation explanation |
| Terraform AWS VPC and EKS | Two public/two private subnets, NAT, managed workers, EBS CSI, restricted API access | Init/validate and mock-provider plan tests only |
| Namespace and Helm package | `k8s/namespace.yaml`, `helm/campuscrate/` | Local install/upgrade and CI deployment |
| Two frontend and backend replicas; ClusterIP | Both Deployments/Services; HPA minimum two | Running-pod and Service captures |
| Ingress `/` and `/api` | Nginx controller plus Helm Ingress | Browser through campuscrate.localhost |
| HPA and CPU requests | CPU target 60%, minimum two, maximum five | Actual 2→5 event; 20m request documented for laptop demo |
| Process liveness vs DB readiness | `/health` and `/ready` | Tests include a DB failure producing readiness 503 |
| Metrics, Prometheus, Grafana | `/metrics`, ServiceMonitor, dashboard and alerts | UP targets and populated dashboard |
| Broken image and wrong Service selector | Separate lab objects and recovery runbook | Actual failures/repair captures; lab objects removed |
| Rollback and troubleshooting | Helm history/rollback instructions and DB rollback caveat | Runbook explains workload versus database recovery |
| README, demo and submission instructions | Root README, demo script, evidence and checklist | Linked from root |

## What is still incomplete

1. **Real AWS evidence:** no real AWS plan, provisioned VPC/EKS, Console screenshot or destroy run. This follows the owner's instruction not to provision. Mock tests do not satisfy those criteria; up to 11 of M7's 15 points depend on real planning/provisioning/destruction, subject to the instructor's evaluation.
2. **Student presentation:** an eight-minute walkthrough is prepared, but the student still needs to present live or record it. A deployment smoke test is not a substitute for demonstrating understanding.
3. **Official form submission:** the Google Form has not been submitted. Use the official SST email, verify the final links and submit once.
4. **Exact evidence format:** command output and clearly labelled browser-viewer screenshots are provided. If the instructor requires a native terminal-window screenshot specifically, capture the documented commands in the student's terminal before submission.

This audit distinguishes implemented components, executed checks and remaining submission requirements. It does not claim a perfect score or a deployed AWS environment.
