import importlib.util, json, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer
import sys
sys.path.insert(0,str(Path(__file__).parent))
spec=importlib.util.spec_from_file_location('review_server',Path(__file__).with_name('server.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
class ReviewTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();s.STATE_FILE=Path(cls.temp.name)/'notes.json';s.FINAL_ROOT=Path(cls.temp.name)/'final-content'
  cls.http=ThreadingHTTPServer(('127.0.0.1',0),s.Handler);cls.base=f'http://127.0.0.1:{cls.http.server_port}'
  threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.temp.cleanup()
 def call(self,path,data=None,headers=None):
  req=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers=headers or {})
  with urllib.request.urlopen(req) as r:return json.load(r)
 def test_plan_approval_is_separate_and_revision_bound(self):
  import os,time
  original_root,original_output=s.ROOT,s.OUTPUT
  try:
   with tempfile.TemporaryDirectory() as temp:
    s.ROOT=Path(temp);s.OUTPUT=s.ROOT/'output';folder=s.OUTPUT/'Plan';folder.mkdir(parents=True)
    video=folder/'Named-source.mp4';video.write_bytes(b'source');os.utime(video,(time.time()-5,time.time()-5))
    plan={'title':'Test AI Flow','verbal_hook':'Recorded hook','visual_hook':'Real interface','strategy':'Demonstrate workflow','rows':[{'text':'All recorded words','start':0,'end':1,'source_start':0,'source_end':1,'edit':'Keep','overlay':'Real UI'}],'required_assets':[]}
    (folder/'edit-plan.json').write_text(json.dumps(plan))
    s.save_state({'notes':[],'approved':{},'registered':{'output/Plan/Named-source.mp4':{'group':'Plan','stage':'source','label':'Named source'}}})
    v=self.call('/api/state')['groups'][0]['versions'][0];r=self.call('/api/plan?video='+v['id'])
    self.call('/api/plan-approve',{'video':v['id'],'revision':r['revision']})
    self.assertTrue(self.call('/api/plan?video='+v['id'])['approved']);self.assertFalse(self.call('/api/state')['groups'][0]['approved'])
    with self.assertRaises(urllib.error.HTTPError):self.call('/api/approve',{'video':v['id']})
    plan['strategy']='Different approved scene needed'
    self.call('/api/plan-save',{'video':v['id'],'revision':r['revision'],'plan':plan})
    updated=self.call('/api/plan?video='+v['id']);self.assertFalse(updated['approved']);self.assertIsNone(updated['queue'])
    with self.assertRaises(urllib.error.HTTPError):self.call('/api/plan-approve',{'video':v['id'],'revision':r['revision']})
    plan['rows'][0]['text']='Changed speech'
    with self.assertRaises(urllib.error.HTTPError):self.call('/api/plan-save',{'video':v['id'],'revision':updated['revision'],'plan':plan})
  finally:s.ROOT,s.OUTPUT=original_root,original_output;s.save_state({'notes':[],'approved':{},'registered':{}})
 def test_version_bound_manual_trims(self):
  import os,time
  from unittest.mock import patch
  from waveform import validate_cuts
  self.assertEqual(validate_cuts([{'start':2,'end':3},{'start':1,'end':2.5}],10),[{'start':1.0,'end':3.0}])
  for cuts in ([{'start':-1,'end':1}],[{'start':0,'end':10}],[{'start':float('nan'),'end':1}]):
   with self.assertRaises(ValueError):validate_cuts(cuts,10)
  original_root,original_output=s.ROOT,s.OUTPUT
  try:
   with tempfile.TemporaryDirectory() as temp:
    s.ROOT=Path(temp);s.OUTPUT=s.ROOT/'output';folder=s.OUTPUT/'Trim';folder.mkdir(parents=True)
    video=folder/'Trim.mp4';video.write_bytes(b'test media');os.utime(video,(time.time()-5,time.time()-5))
    s.save_state({'notes':[],'approved':{},'registered':{}})
    group=self.call('/api/state')['groups'][0];ident=group['latest']
    with patch.object(s,'waveform',return_value={'duration':10,'peaks':[.1],'bins_per_second':100}):
     self.call('/api/trim-save',{'video':ident,'cuts':[{'start':1.1,'end':1.4}]})
     saved=json.loads(s.STATE_FILE.read_text())['trim_requests'][ident]
     self.assertEqual(saved['cuts'],[{'start':1.1,'end':1.4}]);self.assertEqual(saved['group'],group['id']);self.assertEqual(saved['video'],ident)
     self.assertEqual(self.call('/api/waveform?video='+ident)['cuts'],saved['cuts'])
     with self.assertRaises(urllib.error.HTTPError):self.call('/api/trim-save',{'video':'stale version','cuts':[]})
    self.call('/api/remove',{'group':group['id']});self.assertEqual(self.call('/api/state')['groups'],[]);self.assertTrue(video.exists())
    self.call('/api/remove',{'group':group['id'],'removed':False});self.assertEqual(len(self.call('/api/state')['groups']),1)
  finally:s.ROOT,s.OUTPUT=original_root,original_output;s.save_state({'notes':[],'approved':{},'registered':{}})
 @unittest.skip('Needs a saved transcript mapping in script_data.CONFIG; add one for your own video to run it')
 def test_timestamped_script_preserves_words_and_plan(self):
  from script_data import get_script,normalize_words,CONFIG,load
  path='output/sample-project/Sample-V1-final.mp4'
  data=get_script({'path':path,'id':'unit-test','offset':0})
  self.assertEqual(data['status'],'ready');self.assertGreater(len(data['rows']),50)
  original=normalize_words(load(CONFIG[path]['transcript']))
  self.assertEqual(' '.join(w['text'] for w in original),' '.join(r['text'] for r in data['rows']))
  self.assertTrue(all(r['end']>=r['start'] for r in data['rows']))
  self.assertTrue(any(r['start'] is None for r in data['plan']))
  self.assertTrue(all(len([r[k] for k in ('text','edit','overlay')])==3 for r in data['plan']))
 def test_new_draft_discovery_and_approval(self):
  import os,time
  original_root,original_output=s.ROOT,s.OUTPUT
  try:
   with tempfile.TemporaryDirectory() as temp:
    s.ROOT=Path(temp);s.OUTPUT=s.ROOT/'output';folder=s.OUTPUT/'Example';folder.mkdir(parents=True)
    state={'notes':[],'approved':{},'registered':{}}
    first=folder/'Example-v1.mp4';first.write_bytes(b'example');os.utime(first,(time.time()-5,time.time()-5))
    groups=s.catalog(state);self.assertEqual(len(groups),1);state['approved'][groups[0]['latest']]=time.time();self.assertTrue(s.catalog(state)[0]['approved'])
    second=folder/'Example-v2.mp4';second.write_bytes(b'new example');os.utime(second,(time.time()-5,time.time()-5))
    groups=s.catalog(state);self.assertFalse(groups[0]['approved']);self.assertEqual(len(groups[0]['versions']),2)
    state['shipped']=[v['id'] for v in groups[0]['versions']];self.assertEqual(s.catalog(state),[]);state['shipped']=[]
    state['removed_groups']={groups[0]['id']:{'at':time.time()}};self.assertEqual(s.catalog(state),[]);self.assertTrue(first.exists());self.assertTrue(second.exists());state['removed_groups']={}
    mask=folder/'mask.mp4';mask.write_bytes(b'not a draft');self.assertEqual(len(s.catalog(state)[0]['versions']),2)
  finally:s.ROOT,s.OUTPUT=original_root,original_output
 @unittest.skipUnless(any((Path(__file__).resolve().parent.parent/'output').rglob('*.mp4')) if (Path(__file__).resolve().parent.parent/'output').exists() else False, 'Needs a finished draft with a cover in output/')
 def test_workflow_and_seek(self):
  state=self.call('/api/state');g=next(g for g in state['groups'] if any(v['id']==g['latest'] and v.get('cover') and not v['clip'] and v.get('stage')!='source' for v in g['versions']));v=next(v for v in g['versions'] if v['id']==g['latest'])
  self.call('/api/note',{'video':v['id'],'start':14.2,'end':16.5,'text':'Move the overlay away from the face.','script':'The related script passage.'})
  saved=json.loads(s.STATE_FILE.read_text());n=saved['notes'][0];self.assertEqual(n['path'],v['path']);self.assertEqual(n['end'],16.5);self.assertEqual(n['script'],'The related script passage.')
  self.call('/api/note-update',{'id':n['id'],'resolved':True});self.assertTrue(self.call('/api/state')['notes'][0]['resolved'])
  self.call('/api/approve',{'video':v['id']});delivery=json.loads(s.STATE_FILE.read_text())['approved'][v['id']]['delivery'];self.assertTrue(Path(delivery['video']).is_file());self.assertTrue(Path(delivery['cover']).is_file());self.assertTrue((s.ROOT/v['path']).is_file());self.assertTrue(next(x for x in self.call('/api/state')['groups'] if x['id']==g['id'])['approved'])
  self.call('/api/approve',{'video':v['id'],'approved':False});self.assertFalse(next(x for x in self.call('/api/state')['groups'] if x['id']==g['id'])['approved'])
  self.call('/api/note-update',{'id':n['id'],'delete':True});self.assertEqual(self.call('/api/state')['notes'],[])
  from urllib.parse import quote
  req=urllib.request.Request(self.base+'/media?path='+quote(v['path']),headers={'Range':'bytes=10-41'})
  with urllib.request.urlopen(req) as r:
   self.assertEqual(r.status,206);self.assertEqual(len(r.read()),32)
  self.call('/api/register',{'path':'output/tesseract-setup-check-20261009/Setup.mp4','group':g['id'],'clip':True,'offset':14.2,'label':'Scene check'})
  versions=next(x for x in self.call('/api/state')['groups'] if x['id']==g['id'])['versions']
  self.assertTrue(any(x['clip'] and x['offset']==14.2 for x in versions))
  for path in ['/media?path=review-panel/server.py','/media?path=output/../../activate.sh']:
   with self.assertRaises(urllib.error.HTTPError):self.call(path)
  with self.assertRaises(urllib.error.HTTPError) as caught:self.call('/api/approve',{'video':v['id']},headers={'Origin':'https://example.com'})
  self.assertEqual(caught.exception.code,403)
if __name__=='__main__':unittest.main()
