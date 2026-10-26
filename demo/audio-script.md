# CampusCrate narration

Narration by Praneeth Budati.

---

Hi, I'm Praneeth Budati. This is CampusCrate, my DevOps capstone project. It manages shared campus equipment, including inventory, borrowing, returns and loan history.

Let me demonstrate the application. I'm adding a wireless microphone, setting its quantity to two and assigning it to the AV room. The inventory updates immediately. Next, I select the microphone, enter the borrower's name and choose a return deadline. Confirming the loan reduces availability and creates an active loan. Returning the equipment restores the available stock while keeping the completed loan in the ledger.

The frontend uses React, and the backend uses FastAPI. Swagger documents the REST endpoints for inventory and loans. PostgreSQL stores the data, while Alembic manages database migrations. Transactions and row locking protect equipment availability when multiple borrowers submit requests together.

Docker Compose starts the frontend, backend and database. Startup checks ensure that PostgreSQL becomes healthy and migrations finish before the application serves requests. The recorded PostgreSQL test run passed eighteen tests with ninety-point-two-two percent overall statement coverage, including concurrent borrowing and duplicate-return scenarios.

Here is a recorded successful GitHub Actions run. The workflow runs tests, builds both container images and scans them with Trivy. The security gate blocks HIGH and CRITICAL findings. Successful images receive Git commit SHA tags in GitHub Container Registry, connecting each image to its source revision. A temporary Kubernetes deployment then runs an application smoke test.

Helm packages the Kubernetes configuration. The deployment includes frontend and backend replicas, internal Services, Ingress routing and persistent PostgreSQL storage. The backend's autoscaler has a minimum of two replicas and a maximum of five. The recorded load demonstration shows it scaling to five.

Prometheus collects application metrics, and the recorded Grafana dashboard shows request rate, latency and errors. Troubleshooting exercises cover incorrect image tags and Service selectors.

Terraform defines the AWS VPC and EKS infrastructure. Configuration validation and mock-provider tests passed, but real AWS resources were not provisioned.

The repository contains the application, deployment configuration, documentation and supporting evidence. Thank you.
