# Native Terminal screenshots

Open `scripts/native-evidence.command` in macOS Terminal. It runs read-only checks of
the current Compose stack, Kubernetes workloads, routing, HPA, Helm release,
deployed application revision and Git history. Failed commands remain visible
with their actual exit status.

For each page, press **Shift-Command-4**, then **Space**, then click the Terminal
window. Save with the filename displayed on that page. Press Return only after
saving the screenshot. Output is paginated to the window height so nothing is
clipped. A wider Terminal window makes Kubernetes tables easier to read.

To include the previously recorded test, monitoring, troubleshooting, Terraform
and security outputs, run from the project root:

```sh
./scripts/native-evidence.command all
```

Recorded transcripts are visibly labelled **SAVED RUN TRANSCRIPT**. They are
evidence of the recorded run, not a new execution. The default `live` mode runs
the checks again; `saved` displays only those recorded transcripts. This workflow
does not provision AWS, deploy infrastructure, edit application data, or capture
screenshots automatically.

Inspect the PNGs, move them into `evidence/`, and update the evidence index with
the files actually captured. Keep the existing output-viewer labels until native
screenshots have been captured and verified.
