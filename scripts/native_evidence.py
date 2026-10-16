"""Present real command output for manually captured native Terminal evidence."""

import argparse
from datetime import datetime
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LIVE = [
    ("compose", ["docker", "compose", "ps"]),
    ("readiness", ["curl", "--fail", "--silent", "--show-error", "--max-time", "10", "http://127.0.0.1:8001/ready"]),
    ("workloads", ["kubectl", "-n", "campuscrate", "get", "pods,deploy,statefulset"]),
    ("routing-and-scaling", ["kubectl", "-n", "campuscrate", "get", "svc,ingress,hpa"]),
    ("helm", ["helm", "list", "-n", "campuscrate"]),
    ("deployed-release", ["kubectl", "-n", "campuscrate", "exec", "deployment/backend", "--", "python", "-c", "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').read().decode())"]),
    ("history", ["git", "log", "-20", "--format=%h %an | %s"]),
]
SAVED = [
    "pytest.txt", "metrics.txt", "hpa-scale-up.txt", "hpa-events.txt",
    "broken-image.txt", "service-before.txt", "service-after.txt",
    "terraform-validate.txt", "terraform-mock-tests.txt",
    "security-backend/trivy-backend.txt", "security-frontend/trivy-frontend.txt",
]


def present(name, description, output):
    """Keep every output line visible, splitting at the actual terminal height."""
    size = shutil.get_terminal_size((100, 24))
    # Account for wrapped lines as well as explicit newlines.
    lines = []
    width = max(20, size.columns - 1)
    for line in output.expandtabs(4).splitlines():
        if line:
            lines.extend(line[i:i + width] for i in range(0, len(line), width))
        else:
            lines.append("")
    height = max(1, size.lines - 10)
    pages = [lines[i:i + height] for i in range(0, len(lines), height)] or [["(no output)"]]
    for index, page in enumerate(pages, 1):
        print("\033[2J\033[H", end="", flush=True)
        print(f"CampusCrate | {name} | page {index}/{len(pages)}")
        print(datetime.now().astimezone().isoformat(timespec="seconds"))
        # Keep a long command from wrapping outside the reserved header space.
        print(description[:width])
        print("-" * min(width, 100))
        print("\n".join(page))
        print(f"\nSave as native-{name}-{index:02d}.png")
        print("macOS: Shift-Command-4, then Space, then click this Terminal window.")
        input("After saving the screenshot, press Return for the next page (Ctrl-C stops). ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("live", "saved", "all"), default="live")
    parser.add_argument("--list", action="store_true", help="List evidence without executing commands")
    args = parser.parse_args()
    if args.list:
        for name, command in LIVE:
            print(f"LIVE {name}: {shlex.join(command)}")
        for filename in SAVED:
            print(f"SAVED evidence/{filename}")
        return 0
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        parser.error("Open scripts/native-evidence.command in Terminal; an interactive window is required.")
    if args.mode in ("live", "all"):
        for name, command in LIVE:
            try:
                result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, timeout=45, check=False)
                output = result.stdout + f"\nExit status: {result.returncode}"
            except (OSError, subprocess.TimeoutExpired) as error:
                output = f"Command could not complete: {error}"
            present(name, "$ " + shlex.join(command), output)
    if args.mode in ("saved", "all"):
        for filename in SAVED:
            path = ROOT / "evidence" / filename
            output = path.read_text() if path.is_file() else "Evidence file is missing."
            present(path.stem, "SAVED RUN TRANSCRIPT: evidence/" + filename, output)
    print("Finished. Move your saved native-*.png captures into evidence/ after checking them.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nCapture session stopped.")
        raise SystemExit(130)
