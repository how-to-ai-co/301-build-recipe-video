import React from 'react';
import {Composition,registerRoot,useCurrentFrame,interpolateColors} from 'remotion';
// Adapted from the user's battery.html: transparent, slim enough to fit beneath the face.
const Battery: React.FC=()=>{
 const frame=useCurrentFrame(); const p=Math.min(1,frame/89);
 const fill=interpolateColors(p,[0,.5,1],['#e5484d','#f5a524','#30c85e']);
 return <div style={{width:560,height:190,background:'transparent',fontFamily:'Arial, sans-serif'}}>
  <svg width={560} height={190} viewBox="0 0 560 190">
   <text x="280" y="47" textAnchor="middle" fontSize="34" fontWeight="600" fill="#fff" stroke="#171717" strokeWidth="4" paintOrder="stroke" opacity={Math.floor(frame/12)%2===0?1:.18}>using less AI..</text>
   <rect x="10" y="80" width="500" height="105" rx="25" fill="none" stroke="#e8edf2" strokeWidth="10"/>
   <path d="M 530 109 H 540 Q 550 109 550 119 V 145 Q 550 155 540 155 H 530 Z" fill="#e8edf2"/>
   {p>0&&<rect x="28" y="98" width={464*p} height="69" rx="12" fill={fill}/>}
   <text x="260" y="146" textAnchor="middle" fontSize="38" fontWeight="600" fill="#e8edf2" stroke="#172019" strokeWidth="3" paintOrder="stroke">{Math.round(p*100)}%</text>
  </svg>
 </div>;
};
registerRoot(()=> <Composition id="Battery" component={Battery} width={560} height={190} fps={30} durationInFrames={90}/>);
