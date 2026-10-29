#!/usr/bin/env python3
"""Render a silent Tesseract visual spot-check without rendering the full edit."""
import argparse,json,shutil,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CLI=Path.home()/'Library/Application Support/Tesseract/bin/tsrct'
def run(*args):return subprocess.run([str(CLI),*map(str,args)],check=True,capture_output=True,text=True)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--start',type=float,required=True);p.add_argument('--end',type=float,required=True);p.add_argument('--group',required=True);p.add_argument('--name',default='Scene check');p.add_argument('--port',type=int,default=8766);a=p.parse_args()
if a.start<0 or a.end<=a.start:p.error('Require 0 <= start < end')
import uuid
folder=ROOT/'output'/'scene-previews'/uuid.uuid4().hex[:10];folder.mkdir(parents=True,exist_ok=False)
work=folder/'.tesseract-work';work.mkdir()
project=folder/'Scene.tsrct';shutil.copy2(a.project,project)
edit=work/'editable.json';run('project','checkout','--project',project,'--output',edit)
doc=json.loads(edit.read_text());comp=doc['composition']
if a.end>doc['duration']:p.error('Range extends beyond project duration')
def ids(layers):
 for layer in layers:
  yield layer['id'];yield from ids(layer.get('layers',[]))
groupid=max(ids(comp['layers']),default=0)+1
# Native grouping preserves linked effects and original layer clocks.
actions=[{'type':'groupFxCompositionLayers','compositionId':comp['id'],'layerIds':[x['id'] for x in comp['layers']],
          'groupLayerId':groupid,'name':'Visual scene spot-check',
          'transform':{'anchorPoint':[0,0],'position':[0,0],'scale':[100,100],'rotation':0,'opacity':100}}]
actionfile=work/'group.json';actionfile.write_text(json.dumps(actions));run('project','apply','--project',project,'--actions',actionfile)
run('project','checkout','--project',project,'--output',edit);doc=json.loads(edit.read_text());group=next(x for x in doc['composition']['layers'] if x['id']==groupid)
start=round(a.start*1000);duration=round((a.end-a.start)*1000)
group['playback']={'type':'windowed','inputRange':{'start':start,'duration':duration},'mapping':{'type':'linear','input':{'start':start,'duration':duration},'output':{'start':start,'duration':duration}},'inputOffsetMs':0}
edit.write_text(json.dumps(doc));run('project','commit','--project',project,'--file',edit)
video=folder/'Scene.mp4';result=run('export','--project',project,'--fx-solo',f'{comp["id"]}:{groupid}','--output',video)
registration={'path':str(video.relative_to(ROOT)),'group':a.group,'label':f'{a.name} ({a.start:.1f}–{a.end:.1f}s; silent)','offset':a.start,'clip':True}
(folder/'review.json').write_text(json.dumps(registration,indent=2))
try:
 req=urllib.request.Request(f'http://127.0.0.1:{a.port}/api/register',data=json.dumps(registration).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req) as r:json.load(r)
except Exception as e:print('Preview rendered; panel registration failed:',e)
print(video)
