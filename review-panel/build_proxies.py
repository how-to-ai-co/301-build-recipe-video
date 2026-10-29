import hashlib,json,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
cache=ROOT/'.cache/review-proxies';cache.mkdir(parents=True,exist_ok=True)
state=json.load(urllib.request.urlopen('http://127.0.0.1:8766/api/state'))
for group in state['groups']:
    v=next(v for v in group['versions'] if v['id']==group['latest'])
    p=ROOT/v['path'];stamp=f'{p}:{p.stat().st_size}:{p.stat().st_mtime_ns}'
    target=cache/(hashlib.sha256(stamp.encode()).hexdigest()+'.mp4')
    if target.exists():continue
    temp=target.with_suffix('.partial.mp4')
    subprocess.run(['ffmpeg','-v','error','-i',str(p),'-vf','scale=540:-2','-c:v','libx264','-preset','ultrafast','-crf','26','-g','6','-keyint_min','6','-sc_threshold','0','-c:a','aac','-b:a','128k','-movflags','+faststart','-threads','2','-y',str(temp)],check=True)
    temp.rename(target);print(group['name'],target.stat().st_size,flush=True)
