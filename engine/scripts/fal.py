#!/usr/bin/env python3
"""fal.ai runner for the video engine. THIS SPENDS REAL MONEY.

Usage:
  python3 scripts/fal.py <endpoint-id> '<json input>' [outfile] [--go]
  python3 scripts/fal.py --upload <file>             # put a local file on fal storage, print its URL
  python3 scripts/fal.py --datauri <image path>      # print a data URI for small image_url fields

  e.g. python3 scripts/fal.py fal-ai/minimax/speech-2.8-hd \
         '{"text":"...","voice_setting":{"voice_id":"English_CaptivatingStoryteller","speed":1.0},"output_format":"url"}' \
         public/audio/vo_101.mp3 --go

Without --go it prints the endpoint and payload and stops. Nothing is spent.
It does NOT print a price: look the model up on fal.ai and tell the operator
the cost before adding --go. parts/55-generation-fal.md has the proven
endpoints and payloads.

KEY ISOLATION: the key is read ONLY from engine/.env next to this scripts
folder. The shell environment is never consulted, so a key exported for
another project can never route through here. Never prints the key.
"""
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

QUEUE = "https://queue.fal.run"
UPLOAD = "https://rest.alpha.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(ROOT, ".env")


def token():
    if not os.path.exists(ENV):
        sys.exit(f"no .env at {ENV}. This engine only reads its own .env.")
    with open(ENV) as f:
        for line in f:
            if line.startswith("FAL_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    sys.exit("FAL_KEY not set in engine/.env")


def datauri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def upload(path, tok):
    # Two steps: ask fal for an upload slot, then PUT the bytes to it. The
    # returned file_url is what video_url / audio_url / image_urls fields want.
    # Use this for video and audio; data URIs are only sane for small images.
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    slot = call(UPLOAD, tok, {"content_type": mime, "file_name": os.path.basename(path)})
    with open(path, "rb") as f:
        req = urllib.request.Request(slot["upload_url"], data=f.read(), method="PUT")
    req.add_header("Content-Type", mime)
    try:
        urllib.request.urlopen(req, timeout=300).close()
    except urllib.error.HTTPError as e:
        sys.exit(f"fal upload {e.code}: {e.read().decode()[:400]}")
    return slot["file_url"]


def call(url, tok, data=None):
    req = urllib.request.Request(url, method="POST" if data is not None else "GET")
    req.add_header("Authorization", f"Key {tok}")
    req.add_header("Content-Type", "application/json")
    body = json.dumps(data).encode() if data is not None else None
    try:
        with urllib.request.urlopen(req, body) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # 403 "User is locked. Reason: Exhausted balance" means top up, not a bad key.
        sys.exit(f"fal {e.code}: {e.read().decode()[:400]}")


def run(endpoint, payload, tok, timeout=900):
    sub = call(f"{QUEUE}/{endpoint}", tok, payload)
    rid = sub.get("request_id")
    if not rid:
        sys.exit(f"no request_id in response: {json.dumps(sub)[:300]}")
    print(f"  request_id {rid}", file=sys.stderr)
    base = "/".join(endpoint.split("/")[:2])
    status_url = sub.get("status_url") or f"{QUEUE}/{base}/requests/{rid}/status"
    response_url = sub.get("response_url") or f"{QUEUE}/{base}/requests/{rid}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = call(status_url, tok)
        state = st.get("status")
        if state == "COMPLETED":
            return call(response_url, tok)
        if state in ("FAILED", "CANCELLED", "ERROR"):
            sys.exit(f"fal job {state}: {json.dumps(st)[:400]}")
        print(f"  {state or '...'}", file=sys.stderr)
        time.sleep(4)
    sys.exit(f"timed out after {timeout}s (request {rid})")


def urls(out):
    found = []
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("url"), str):
                found.append(o["url"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(out)
    return found


def download(url, path):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())


def main():
    args = [a for a in sys.argv[1:] if a != "--go"]
    go = "--go" in sys.argv
    if len(args) == 2 and args[0] == "--datauri":
        print(datauri(args[1]))
        return
    if len(args) == 2 and args[0] == "--upload":
        print(upload(args[1], token()))
        return
    if len(args) < 2:
        sys.exit(__doc__)
    endpoint, payload = args[0], json.loads(args[1])
    outfile = args[2] if len(args) > 2 else None
    timeout = 2400 if "video" in endpoint or "seedance" in endpoint else 900
    if not go:
        shown = {k: (v[:60] + "...[data uri]" if isinstance(v, str) and v.startswith("data:") else v)
                 for k, v in payload.items()}
        print(f"DRY RUN  {endpoint}\n{json.dumps(shown, indent=2)}\n(add --go to spend)")
        return
    tok = token()
    out = run(endpoint, payload, tok, timeout)
    got = urls(out)
    if outfile and got:
        base, ext = os.path.splitext(outfile)
        for i, u in enumerate(got):
            p = outfile if i == 0 else f"{base}_{i}{ext}"
            download(u, p)
            print(p)
    elif got:
        for u in got:
            print(u)
    else:
        print(json.dumps(out)[:600])


if __name__ == "__main__":
    main()
