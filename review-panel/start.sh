#!/bin/zsh
cd "$(dirname "$0")/.." || exit 1
source ./activate.sh
python - <<'PY'
import subprocess, pathlib, urllib.request
root=pathlib.Path.cwd()
try:
    urllib.request.urlopen('http://127.0.0.1:8766/api/state',timeout=2)
    print('Review panel already running: http://127.0.0.1:8766')
except Exception:
    log=(root/'review-panel/server.log').open('a')
    process=subprocess.Popen([str(root/'.venv/bin/python'),'review-panel/server.py'],cwd=root,stdout=log,stderr=log,start_new_session=True)
    (root/'review-panel/server.pid').write_text(str(process.pid))
    print('Started review panel: http://127.0.0.1:8766')
PY
