"""Version-specific timestamped scripts and saved three-column source plans."""
import json,re,subprocess,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CACHE=Path(__file__).parent/'scripts'
JOBS={};JOB_LOCK=threading.Lock();MODEL_LOCK=threading.Lock()
# Optional saved transcript mappings, keyed by video path under output/:
# 'output/my-video/V2-final.mp4': {'transcript': ROOT/'output/my-video/transcript.json', 'map': ..., 'events': ...}
CONFIG={}
def load(p,default=None):return json.loads(p.read_text()) if p and p.exists() else default

def normalize_words(data):
 if isinstance(data,list):return [{'text':w.get('word',w.get('w','')).strip(),'start':float(w.get('start',w.get('s',0))),'end':float(w.get('end',w.get('e',0)))} for w in data]
 words=[]
 for seg in data.get('segments',[]):
  if seg.get('words'):words.extend(normalize_words(seg['words']))
  elif seg.get('text','').strip():words.append({'text':seg['text'].strip(),'start':seg['start'],'end':seg['end']})
 return words

def maps(config):
 data=load(config.get('map'),[])
 if isinstance(data,dict):data=data.get('segments',[])
 return [{'in':v.get('new_in',v.get('output_start')),'out':v.get('new_out',v.get('output_end')),'source_in':v.get('source_in',v.get('source_start')),'source_out':v.get('source_out',v.get('source_end'))} for v in data]

def source_at(t,mapping,end=False):
 candidates=[v for v in mapping if v['in']<=t<=v['out']]
 if not candidates:return None
 v=candidates[0] if end else candidates[-1]
 return v['source_in']+(t-v['in'])/(v['out']-v['in'])*(v['source_out']-v['source_in']) if v['out']>v['in'] else v['source_in']

def chunks(words,events=None,mapping=None):
 result=[];batch=[]
 def emit():
  if not batch:return
  start,end=batch[0]['start'],batch[-1]['end'];mid=(start+end)/2
  event=next((e for e in events or [] if e['in']<=mid<e['out']),None)
  if event:
   concept=event.get('concept','').replace('-',' ').capitalize()
   overlay=concept+(' · '+event['layout'] if event.get('layout') else '')
  else:overlay='No overlay cue recorded'
  result.append({'start':round(start,3),'end':round(end,3),'text':' '.join(w['text'] for w in batch),'source_start':source_at(start,mapping or []),'source_end':source_at(end,mapping or [],True),'edit':'Retained dialogue','overlay':overlay})
 for w in words:
  if not w['text']:continue
  if batch and (w['end']-batch[0]['start']>2.0 or w['start']-batch[-1]['end']>.5):emit();batch=[]
  batch.append(w)
  if w['end']-batch[0]['start']>=1.0 and re.search(r'[.!?]$',w['text']):emit();batch=[]
 emit();return result

def source_plan(config,mapping):
 p=config.get('plan');rows=[]
 if not p or not p.exists():return rows
 for line in p.read_text().splitlines():
  cells=[c.strip() for c in line.strip().strip('|').split('|')]
  if len(cells)!=3:continue
  match=re.match(r'(\d+):(\d+(?:\.\d+)?)–(\d+):(\d+(?:\.\d+)?) · (.*)',cells[0])
  if not match:continue
  a,b,c,d,text=match.groups();start=int(a)*60+float(b);end=int(c)*60+float(d)
  overlaps=[m for m in mapping if m['source_out']>start and m['source_in']<end]
  output_start=output_end=None
  if overlaps:
   first,last=overlaps[0],overlaps[-1]
   def mapped(t,m):return m['in']+(t-m['source_in'])/(m['source_out']-m['source_in'])*(m['out']-m['in'])
   output_start=mapped(max(start,first['source_in']),first);output_end=mapped(min(end,last['source_out']),last)
  rows.append({'start':output_start,'end':output_end,'source_start':start,'source_end':end,'text':text,'edit':cells[1],'overlay':cells[2]})
 return rows

def get_script(video):
 cache=CACHE/(video['id']+'.json')
 if cache.exists():return load(cache)
 cfg=CONFIG.get(video['path'])
 # Explicit video-name sidecars let new edits supply reviewed wording and cues.
 sidecar=(ROOT/video['path']).with_suffix('.review-script.json')
 if sidecar.exists():return load(sidecar)
 if not cfg:return {'status':JOBS.get(video['id'],'missing'),'rows':[],'plan':[]}
 words=normalize_words(load(cfg['transcript']));mapping=maps(cfg)
 if 'retime' in cfg:
  intervals=load(cfg['retime'])['retained_intervals'];retimed=[]
  for w in words:
   overlapping=[v for v in intervals if v['v4_out']>w['start'] and v['v4_in']<w['end']]
   if not overlapping:continue
   a,b=overlapping[0],overlapping[-1];w=dict(w)
   w['start']=a['v5_in']+max(w['start'],a['v4_in'])-a['v4_in'];w['end']=b['v5_in']+min(w['end'],b['v4_out'])-b['v4_in'];retimed.append(w)
  words=retimed
 return {'status':'ready','rows':chunks(words,load(cfg.get('events'),[]),mapping),'plan':source_plan(cfg,mapping),'provenance':'Saved transcription of edited audio; automatic wording may need correction. Source times use the saved cut map.','source':str(cfg['transcript'].relative_to(ROOT))}

def start_transcription(video):
 with JOB_LOCK:
  if JOBS.get(video['id']) in ('queued','transcribing'):return
  JOBS[video['id']]='queued'
 def worker():
  try:
   with MODEL_LOCK:
    JOBS[video['id']]='transcribing';CACHE.mkdir(exist_ok=True)
    audio=CACHE/(video['id']+'.wav')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/video['path']),'-vn','-ar','16000','-ac','1',str(audio)],check=True)
    import whisper
    model=whisper.load_model('small',download_root=str(ROOT/'.cache/whisper'))
    transcript=model.transcribe(str(audio),word_timestamps=True,fp16=False,verbose=False)
    words=normalize_words(transcript)
    for w in words:w['start']+=video.get('offset',0);w['end']+=video.get('offset',0)
    payload={'status':'ready','rows':chunks(words),'plan':[],'provenance':'Automatic local transcription of this exact video. Check names and wording against the audio.','source':video['path']}
    destination=CACHE/(video['id']+'.json');temp=destination.with_suffix('.tmp');temp.write_text(json.dumps(payload,indent=2));temp.replace(destination)
    audio.unlink();JOBS[video['id']]='ready'
  except Exception as e:JOBS[video['id']]='error: '+str(e)
 threading.Thread(target=worker,daemon=True).start()
