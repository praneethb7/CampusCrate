# Security scan record

[Successful delivery run](https://github.com/praneethb7/CampusCrate/actions/runs/38872115532) · commit `056b48f5567576a26e75502633a25b1e87934555`.

Trivy scanned both container images, including their operating-system packages and Python dependencies, and the workflow fails on any HIGH or CRITICAL finding. The final Alpine-based images passed that gate with zero findings at those severities; the raw reports are in [backend](../evidence/security-backend/trivy-backend.txt) and [frontend](../evidence/security-frontend/trivy-frontend.txt). A clean report describes the scanner database and packages at that run; it does not guarantee that future vulnerabilities or application logic flaws do not exist.

## Finding and remediation

The earlier Debian 13.7 backend image was blocked with 44 HIGH/CRITICAL OS-package findings; the Python package section was clean. One reported finding was `CVE-2025-69720` in `ncurses-base`/`ncurses-bin`, described by the scanner as a buffer-overflow vulnerability. Several util-linux findings had no fixed package version in that report, so merely reinstalling application dependencies would not fix the base-image exposure.

The backend was rebuilt on `python:3.12-alpine`, retaining a non-root UID, the migration tooling and the same application tests. The gate remained configured with `exit-code: 1`, `severity: HIGH,CRITICAL` and `ignore-unfixed: false`; no CVE allowlist or scan bypass was added. The subsequent run passed both image scans and the deployed application smoke test.

## Controls and boundaries

- Application runtimes use non-root users. Kubernetes disables privilege escalation and drops capabilities.
- Secrets are generated locally and referenced through Kubernetes Secrets. The local `.env` and Terraform state/variable files are ignored.
- Database is internal to Compose/Kubernetes; the browser calls same-origin `/api` paths.
- Input validation bounds quantities and text, validates enum values and requires timezone-aware future due dates.
- PostgreSQL row locking serializes stock allocation; conflict responses preserve stock and loan history.
- CI uses read-only repository access except for the image-publishing jobs, which need `packages: write`.

This is a classroom administrator application without authentication, authorization, public TLS, rate limiting or production backups. Keep the demo on loopback/trusted networks. Public use would require those controls and a managed secret/backup policy. Kubernetes Secrets are base64 encoded and require cluster RBAC/encryption controls for a production installation.

## Later scan result

[Run 40313700369](https://github.com/praneethb7/CampusCrate/actions/runs/40313700369),
for commit `f673d0233a029f10c203e3ca6fb7b69827f12a42`, blocked publication of the
frontend on 26 October 2026. Its Trivy report identified three HIGH findings in
`brotli-libs`, `curl` and `libcurl`. The listed fixed versions were `1.2.1-r0`
for Brotli and `8.23.0-r0` for curl/libcurl. The security gate remained enabled.
The clean 16 October scan and successful pipeline shown in the presentation and
video are historical evidence, not results from this later run. The frontend
runtime needs package updates and a successful rescan to close these findings.
