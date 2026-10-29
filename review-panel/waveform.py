"""Local waveform cache and validated, version-bound non-destructive cuts."""
import array,json,math,subprocess,sys
from pathlib import Path

def waveform(path,ident,cache):
    cache.mkdir(parents=True,exist_ok=True);target=cache/(ident+'-rms.json')
    if target.exists():return json.loads(target.read_text())
    result=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','s16le','-'],capture_output=True,check=True)
    samples=array.array('h');samples.frombytes(result.stdout)
    if sys.byteorder!='little':samples.byteswap()
    step=80;peaks=[round(max(abs(x) for x in samples[i:i+step])/32768,4) for i in range(0,len(samples),step)]
    rms=[round(math.sqrt(sum(x*x for x in samples[i:i+step])/len(samples[i:i+step]))/32768,5) for i in range(0,len(samples),step)]
    data={'rms':rms,'duration':len(samples)/8000,'bins_per_second':100,'peaks':peaks,'cuts':[]}
    target.write_text(json.dumps(data));return data

def validate_cuts(cuts,duration):
    if not isinstance(cuts,list) or len(cuts)>500:raise ValueError('Invalid cut list')
    ranges=[]
    for cut in cuts:
        a,b=float(cut['start']),float(cut['end'])
        if not all(math.isfinite(t) for t in (a,b)) or not 0<=a<b<=duration+.02:raise ValueError('Cut must be inside this video')
        ranges.append({'start':round(a,3),'end':round(min(b,duration),3)})
    merged=[]
    for c in sorted(ranges,key=lambda c:c['start']):
        if merged and c['start']<=merged[-1]['end']:merged[-1]['end']=max(c['end'],merged[-1]['end'])
        else:merged.append(c)
    if sum(c['end']-c['start'] for c in merged)>=duration-.05:raise ValueError('Keep some footage; cannot cut the entire video')
    return merged
