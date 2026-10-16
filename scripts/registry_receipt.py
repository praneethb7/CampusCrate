"""Capture anonymous GHCR pullability and the published SHA-tag digest."""

import json
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

sha = sys.argv[1]
component = sys.argv[2]
if not re.fullmatch(r"[0-9a-f]{40}", sha) or component not in ("backend", "frontend"):
    raise SystemExit("Expected a full commit SHA and backend or frontend")
repository = (
    "praneethb7/"
    + {"backend": "campuscrate-api", "frontend": "campuscrate-web"}[component]
)
query = urlencode({"service": "ghcr.io", "scope": f"repository:{repository}:pull"})
with urlopen(f"https://ghcr.io/token?{query}", timeout=30) as response:
    token = json.load(response)["token"]
request = Request(
    f"https://ghcr.io/v2/{repository}/manifests/{sha}",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.oci.image.index.v1+json,application/vnd.oci.image.manifest.v1+json,application/vnd.docker.distribution.manifest.v2+json",
    },
)
with urlopen(request, timeout=30) as response:
    manifest = json.load(response)
    digest = response.headers["Docker-Content-Digest"]
if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest or ""):
    raise SystemExit("Registry did not return a valid content digest")
print(
    json.dumps(
        {
            "image": f"ghcr.io/{repository}:{sha}",
            "digest": digest,
            "media_type": manifest["mediaType"],
            "anonymous_pull": True,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        },
        indent=2,
    )
)
