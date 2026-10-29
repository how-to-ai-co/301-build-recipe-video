#!/usr/bin/env python3
"""Local, file-backed video review. No dependencies or external services."""
import argparse, hashlib, json, mimetypes, os, re, threading, time, uuid, shutil, tempfile, subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

from waveform import waveform, validate_cuts
from script_data import get_script, start_transcription

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'output'
HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / 'notes.json'
FINAL_ROOT = Path.home() / 'Desktop' / 'Final Content'
LOCK = threading.RLock()

def read_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {'notes': [], 'approved': {}, 'registered': {}}

def save_state(state):
    temp = STATE_FILE.with_suffix('.tmp')
    temp.write_text(json.dumps(state, indent=2) + '\n')
    os.replace(temp, STATE_FILE)

def media_path(value):
    p = (ROOT / value).resolve()
    if not p.is_relative_to(OUTPUT.resolve()) or not p.is_file() or p.suffix.lower() not in ('.mp4', '.mov', '.webm', '.m4v'):
        raise ValueError('Video must be an existing file inside output/')
    return p

def image_path(value):
    p = (ROOT / value).resolve()
    if not p.is_relative_to(OUTPUT.resolve()) or not p.is_file() or p.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):
        raise ValueError('Cover must be an existing image inside output/')
    return p

def find_cover(video, state):
    custom=state['registered'].get(video['path'],{})
    if custom.get('stage') == 'source': return None
    if custom.get('cover'):
        try:return str(image_path(custom['cover']).relative_to(ROOT))
        except ValueError:return None
    p=ROOT/video['path']
    stem=re.sub(r'-(final|native|draft)$','',p.stem,flags=re.I)
    for ext in ('.png','.jpg','.jpeg','.webp'):
        candidate=p.with_name(stem+'-cover'+ext)
        if candidate.exists():return str(candidate.relative_to(ROOT))
    return None

def deliver(video):
    if video['clip']:raise ValueError('Approve the full video, not a scene preview')
    if not video.get('cover'):raise ValueError('A matching cover is required before approval')
    source=media_path(video['path']);cover=image_path(video['cover'])
    FINAL_ROOT.mkdir(parents=True,exist_ok=True)
    destination=FINAL_ROOT/(source.stem+'-'+video['id'][:8]+'-'+fingerprint(cover)[:6])
    if destination.exists():
        manifest=destination/'delivery.json'
        if manifest.exists() and json.loads(manifest.read_text()).get('video_id')==video['id'] and (destination/source.name).is_file() and (destination/cover.name).is_file():
            return {'folder':str(destination),'video':str(destination/source.name),'cover':str(destination/cover.name)}
        raise ValueError('Delivery folder already exists; existing files were preserved')
    stage=Path(tempfile.mkdtemp(prefix='.pending-',dir=FINAL_ROOT))
    try:
        shutil.copy2(source,stage/source.name);shutil.copy2(cover,stage/cover.name)
        record={'video_id':video['id'],'source_video':str(source),'source_cover':str(cover),'approved_at':time.time()}
        (stage/'delivery.json').write_text(json.dumps(record,indent=2)+'\n')
        stage.rename(destination)
    except Exception:
        shutil.rmtree(stage);raise
    return {'folder':str(destination),'video':str(destination/source.name),'cover':str(destination/cover.name)}

def fingerprint(p):
    s = p.stat()
    return hashlib.sha256(f'{p.relative_to(ROOT)}:{s.st_size}:{s.st_mtime_ns}'.encode()).hexdigest()[:24]

def plan_file(video):
    return media_path(video['path']).parent/'edit-plan.json'

def plan_record(video, state):
    p=plan_file(video)
    if not p.exists():return None
    plan=json.loads(p.read_text())
    revision=hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()
    approval=state.get('plan_approvals',{}).get(video['group'])
    approved=bool(approval and approval['revision']==revision and approval['video']==video['id'])
    return {'plan':plan,'revision':revision,'approved':approved,'queue':state.get('edit_queue',{}).get(video['group'])}

def catalog(state):
    rows = []
    skip = {'assets', 'versions', 'previews', 'scene-renders', 'title-experiments', 'review', 'checks', 'scene-previews', 'style-references', '.tesseract-work'}
    for p in OUTPUT.rglob('*'):
        if p.suffix.lower() not in ('.mp4', '.mov', '.webm', '.m4v') or not p.is_file(): continue
        rel = str(p.relative_to(ROOT)); parts = p.relative_to(OUTPUT).parts
        custom = state['registered'].get(rel)
        if not custom:
            # Batch sources/drafts enter through intake or completed-export registration.
            # Do not show unfinished encodes or technical intermediates as new projects.
            if parts[0].startswith('batch-'):continue
            if any(part.lower() in skip or part.startswith('.') for part in parts[:-1]): continue
            if 'setup-check' in rel or p.stem.startswith('setup-') or re.search(r'(mask|proxy|background|before-|^base$|^scene-|preview|^composite|^dario-test)', p.stem, re.I): continue
            if 'native' in p.stem.lower() and p.with_name(p.name.replace('native','final')).exists(): continue
            group = '/'.join(parts[:2]) if parts[0].startswith('three-yaps') else re.sub(r'-v\d+$', '', parts[0] if len(parts)>1 else p.stem, flags=re.I)
        else: group = custom['group']
        if p.stat().st_size == 0 or time.time()-p.stat().st_mtime < 2: continue
        rows.append({'id':fingerprint(p), 'path':rel, 'name':custom.get('label',p.stem) if custom else p.stem,
                     'group':group, 'offset':custom.get('offset',0) if custom else 0,
                     'clip':bool(custom and custom.get('clip')), 'mtime':p.stat().st_mtime,
                     'approved':fingerprint(p) in state['approved']})
    # Explicit registrations include otherwise excluded assets and previews.
    present = {r['path'] for r in rows}
    for rel, custom in state['registered'].items():
        if rel in present: continue
        try: p=media_path(rel)
        except ValueError: continue
        rows.append({'id':fingerprint(p),'path':rel,'name':custom.get('label',p.stem),'group':custom['group'],
                     'offset':custom.get('offset',0),'clip':bool(custom.get('clip')),'mtime':p.stat().st_mtime,'approved':fingerprint(p) in state['approved']})
    shipped=set(state.get('shipped',[]))
    rows=[r for r in rows if r['id'] not in shipped and r['group'] not in state.get('removed_groups',{})]
    for r in rows:
        r['stage']=state['registered'].get(r['path'],{}).get('stage','draft')
        r['cover']=find_cover(r,state)
        approval=state['approved'].get(r['id'])
        r['delivery']=approval.get('delivery') if isinstance(approval,dict) else None
    def rank(r):
        versions = re.findall(r'(?:revision-|[ -]v|/v)(\d+)',r['path'],re.I)
        return (max(map(int, versions),default=0), int('final' in r['name'].lower()),r['mtime'])
    groups=[]
    for key in sorted({r['group'] for r in rows}):
        versions=sorted([r for r in rows if r['group']==key],key=rank,reverse=True)
        full=[r for r in versions if not r['clip']]
        latest=(full or versions)[0]
        display=state.get('project_names',{}).get(key,key.split('/')[-1].replace('-',' '))
        groups.append({'id':key,'name':display,'latest':latest['id'],'approved':latest['approved'],'versions':versions})
    groups.sort(key=lambda g:max(r['mtime'] for r in g['versions']),reverse=True)
    return groups

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def reply(self, obj, status=200):
        data=json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(data)
    def valid_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
    def do_GET(self):
        if not self.valid_host():return self.reply({'error':'Local host required'},403)
        req=urlparse(self.path)
        if req.path=='/api/state':
            with LOCK:
                state=read_state(); self.reply({'groups':catalog(state),'notes':state['notes'],'finalFolder':str(FINAL_ROOT)})
        elif req.path=='/api/waveform':
            ident=parse_qs(req.query).get('video',[''])[0]
            with LOCK:
                state=read_state();video=next((v for g in catalog(state) for v in g['versions'] if v['id']==ident),None)
            if not video:return self.reply({'error':'Video not found'},404)
            try:
                data=waveform(media_path(video['path']),ident,ROOT/'.cache'/'review-waveforms')
                data={**data,'cuts':state.get('trim_requests',{}).get(ident,{}).get('cuts',[])}
                self.reply(data)
            except Exception as e:self.reply({'error':'Waveform unavailable: '+str(e)},400)
        elif req.path=='/api/script':
            with LOCK:
                ident=parse_qs(req.query).get('video',[''])[0]
                video=next((v for g in catalog(read_state()) for v in g['versions'] if v['id']==ident),None)
            if video:self.reply(get_script(video))
            else:self.reply({'error':'Video not found'},404)
        elif req.path=='/api/plan':
            with LOCK:
                state=read_state();ident=parse_qs(req.query).get('video',[''])[0]
                video=next((v for g in catalog(state) for v in g['versions'] if v['id']==ident),None)
                if not video:return self.reply({'error':'Video not found'},404)
                self.reply(plan_record(video,state) or {'plan':None})
        elif req.path=='/image':
            try:p=image_path(parse_qs(req.query).get('path',[''])[0])
            except ValueError as e:return self.reply({'error':str(e)},404)
            data=p.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(p.name)[0]);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        elif req.path in ('/media','/preview'):
            try: p=media_path(parse_qs(req.query).get('path',[''])[0])
            except ValueError as e: return self.reply({'error':str(e)},404)
            if req.path=='/preview':
                stamp=f'{p}:{p.stat().st_size}:{p.stat().st_mtime_ns}'
                proxy=ROOT/'.cache'/'review-proxies'/(hashlib.sha256(stamp.encode()).hexdigest()+'.mp4')
                if proxy.exists():p=proxy
                elif not proxy.with_suffix('.building').exists():
                    proxy.parent.mkdir(parents=True,exist_ok=True)
                    marker=proxy.with_suffix('.building');marker.touch()
                    def build_preview(source=p,target=proxy,marker=marker):
                        temp=target.with_suffix('.partial.mp4')
                        try:
                            subprocess.run(['ffmpeg','-v','error','-i',str(source),'-vf','scale=540:-2','-c:v','libx264','-preset','ultrafast','-crf','26','-g','6','-keyint_min','6','-sc_threshold','0','-c:a','aac','-b:a','128k','-movflags','+faststart','-threads','2','-y',str(temp)],check=True)
                            temp.replace(target)
                        finally:marker.unlink(missing_ok=True)
                    threading.Thread(target=build_preview,daemon=True).start()
            size=p.stat().st_size; start=0; end=size-1; partial=False
            value=self.headers.get('Range')
            if value:
                match=re.fullmatch(r'bytes=(\d*)-(\d*)',value)
                if not match or not any(match.groups()): return self.reply({'error':'Invalid range'},416)
                a,b=match.groups()
                if a: start=int(a); end=min(int(b),end) if b else end
                else: start=max(0,size-int(b))
                if start> end or start>=size:
                    self.send_response(416); self.send_header('Content-Range',f'bytes */{size}'); self.end_headers(); return
                partial=True
            self.send_response(206 if partial else 200); self.send_header('Content-Type',mimetypes.guess_type(p.name)[0] or 'video/mp4'); self.send_header('Accept-Ranges','bytes'); self.send_header('Content-Length',str(end-start+1))
            if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.end_headers()
            try:
                with p.open('rb') as f:
                    f.seek(start); remaining=end-start+1
                    while remaining:
                        chunk=f.read(min(1024*1024,remaining))
                        if not chunk:break
                        self.wfile.write(chunk); remaining-=len(chunk)
            except (BrokenPipeError,ConnectionResetError):pass
        elif req.path=='/trim-timeline.js':
            data=(HERE/'trim-timeline.js').read_bytes();self.send_response(200);self.send_header('Content-Type','text/javascript');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        elif req.path in ('/','/index.html'):
            data=(HERE/'index.html').read_bytes(); self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        else:self.reply({'error':'Not found'},404)
    def do_POST(self):
        if not self.valid_host():return self.reply({'error':'Local host required'},403)
        # Local mutations are allowed only from this panel's origin.
        if self.headers.get('Origin') not in (None, f'http://{self.headers.get("Host")}'):
            return self.reply({'error':'Invalid origin'},403)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length>100000:return self.reply({'error':'Request too large'},413)
            body=json.loads(self.rfile.read(length)); route=urlparse(self.path).path
            with LOCK:
                state=read_state()
                if route=='/api/trim-save':
                    video=next((v for g in catalog(state) for v in g['versions'] if v['id']==body['video']),None)
                    if not video:raise ValueError('Video version changed; reload before saving')
                    data=waveform(media_path(video['path']),video['id'],ROOT/'.cache'/'review-waveforms')
                    cuts=validate_cuts(body['cuts'],data['duration'])
                    state.setdefault('trim_requests',{})[video['id']]={'video':video['id'],'path':video['path'],'group':video['group'],'cuts':cuts,'status':'saved_for_edit','at':time.time(),'time_basis':'this exact reviewed file; add registered offset for full-output times','offset':video.get('offset',0)}
                elif route=='/api/transcribe':
                    video=next((v for g in catalog(state) for v in g['versions'] if v['id']==body['video']),None)
                    if not video:raise ValueError('Video not found')
                    start_transcription(video)
                elif route in ('/api/plan-save','/api/plan-approve'):
                    video=next((v for g in catalog(state) for v in g['versions'] if v['id']==body['video']),None)
                    if not video:raise ValueError('Video not found')
                    record=plan_record(video,state)
                    if not record:raise ValueError('No edit plan yet')
                    if body.get('revision')!=record['revision']:raise ValueError('Plan changed; reload before saving or approving')
                    if route=='/api/plan-save':
                        plan=body['plan']
                        if not isinstance(plan,dict) or not all(plan.get(k) for k in ('title','verbal_hook','visual_hook','strategy','rows')):raise ValueError('Title, hooks, strategy and full script are required')
                        if not isinstance(plan['rows'],list) or len(plan['rows'])!=len(record['plan']['rows']):raise ValueError('Preserve the complete script; edit proposals instead')
                        for old,new in zip(record['plan']['rows'],plan['rows']):
                            if any(old.get(k)!=new.get(k) for k in ('text','start','end','source_start','source_end')):raise ValueError('Source script and timestamps must stay intact')
                        temp=plan_file(video).with_suffix('.tmp');temp.write_text(json.dumps(plan,indent=2));os.replace(temp,plan_file(video))
                        state.setdefault('plan_approvals',{}).pop(video['group'],None)
                        state.setdefault('edit_queue',{}).pop(video['group'],None)
                    else:
                        state.setdefault('plan_approvals',{})[video['group']]={'video':video['id'],'revision':record['revision'],'at':time.time()}
                        state.setdefault('edit_queue',{})[video['group']]={'video':video['path'],'plan':str(plan_file(video).relative_to(ROOT.resolve())),'revision':record['revision'],'status':'approved_pending_assets' if record['plan'].get('required_assets') else 'queued','at':time.time()}
                elif route=='/api/note':
                    video=next((v for g in catalog(state) for v in g['versions'] if v['id']==body['video']),None)
                    if not video:raise ValueError('Draft no longer exists; refresh and try again')
                    start=float(body['start']); end=body.get('end'); end=float(end) if end is not None else None
                    if not (0<=start<86400) or (end is not None and not start<=end<86400):raise ValueError('Invalid timestamp range')
                    text=str(body['text']).strip()
                    if not text:raise ValueError('Write a note first')
                    state['notes'].append({'id':uuid.uuid4().hex,'video':video['id'],'path':video['path'],'group':video['group'],'start':start,'end':end,'text':text[:10000],'script':str(body.get('script') or '')[:10000],'resolved':False,'created':time.time()})
                elif route=='/api/note-update':
                    note=next(n for n in state['notes'] if n['id']==body['id'])
                    if body.get('delete'):state['notes'].remove(note)
                    elif 'text' in body:
                        text=str(body['text']).strip()
                        if not text:raise ValueError('Note cannot be empty')
                        note['text']=text[:10000]
                    else:note['resolved']=bool(body['resolved'])
                elif route=='/api/remove':
                    group=str(body['group'])
                    if body.get('removed',True):
                        if not any(g['id']==group for g in catalog(state)):raise ValueError('Project not found; refresh first')
                        state.setdefault('removed_groups',{})[group]={'at':time.time()}
                    else:state.setdefault('removed_groups',{}).pop(group,None)
                elif route=='/api/approve':
                    if body.get('approved',True):
                        video=next((v for g in catalog(state) for v in g['versions'] if v['id']==body['video']),None)
                        if not video:raise ValueError('Video not found')
                        if video.get('stage')=='source':raise ValueError('Source footage is not a finished edit; approve the edit plan first')
                        delivery=deliver(video)
                        state['approved'][body['video']]={'at':time.time(),'delivery':delivery}
                    else:state['approved'].pop(body['video'],None)
                elif route=='/api/register':
                    p=media_path(body['path']); rel=str(p.relative_to(ROOT)); offset=float(body.get('offset',0))
                    if offset<0:raise ValueError('Offset must be nonnegative')
                    state['registered'][rel]={'group':str(body['group']),'label':str(body.get('label',p.stem)),'offset':offset,'clip':bool(body.get('clip',False)),'cover':str(image_path(body['cover']).relative_to(ROOT)) if body.get('cover') else None}
                else:return self.reply({'error':'Not found'},404)
                save_state(state)
            self.reply({'ok':True})
        except (ValueError,KeyError,StopIteration,TypeError,OSError) as e:self.reply({'error':str(e) or 'Record not found'},400)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8766);args=parser.parse_args()
    print(f'Video review: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
