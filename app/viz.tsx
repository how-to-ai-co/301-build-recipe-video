import type { CSSProperties } from "react";

const css = (v: Record<string, string | number>) => v as CSSProperties;

export function Bring() {
  return <div className="viz viz-bring">
    <ul className="chips">
      {["instagram.com/reel/…", "IMG_4021.MOV", "yoursite.com"].map((c, i) => <li key={c} className="chip" style={css({ "--i": i })}><i />{c}</li>)}
    </ul>
    <div className="phone"><span className="glow" /></div>
  </div>;
}

export function Study() {
  return <div className="viz viz-study">
    <div className="sheet">{Array.from({ length: 18 }, (_, i) => <span key={i} style={css({ "--i": i })} />)}</div>
    <div className="stats"><b>0.9s per shot</b><b>3-word hook</b><b>captions synced</b></div>
  </div>;
}

export function Plan() {
  const rows = [
    ["0:00 Most people use AI wrong", "Keep", "Title: USE AI"],
    ["0:02 um, so basically", "Cut", ""],
    ["0:04 Here's what works", "Speed 1.05×", "Chart holds 2s"],
    ["0:07 Try it today", "Keep", "Call to action"],
  ];
  return <div className="viz viz-plan">
    <div className="row head"><span>Script</span><span>Edit</span><span>Overlay</span></div>
    {rows.map((r, i) => <div key={i} className="row" style={css({ "--i": i })}>
      <span className={r[1] === "Cut" ? "cut" : ""}>{r[0]}</span><span>{r[1]}</span><span>{r[2] || "—"}</span>
    </div>)}
  </div>;
}

export function Draft() {
  const meters = [["Hook", "0.8s"], ["Safe zone", "100%"], ["Loudness", "−14 LUFS"]];
  return <div className="viz viz-draft">
    <div className="frame"><span className="title">USE AI</span><span className="cap">here&apos;s what <b>works</b></span></div>
    <ul className="meters">
      {meters.map(([k, v], i) => <li key={k} style={css({ "--i": i })}><span>{k}</span><b>{v}</b><i /></li>)}
    </ul>
  </div>;
}

export function Learn() {
  return <div className="viz viz-learn">
    <p className="bubble q">Make the title bigger</p>
    <span className="arrow">→</span>
    <div className="rules">
      <b>Your edit rules</b>
      <span>Cut every pause over 0.3s?</span>
      <span>Captions two lines max?</span>
      <span className="new">Title fills most of the width? [Oct 30]</span>
    </div>
  </div>;
}

// A raw take: words, with pauses and ums that collapse out.
export function Cut() {
  const segs: [string, number][] = [["w", 7], ["g", 3], ["w", 5], ["u", 3], ["w", 8], ["g", 4], ["w", 6]];
  let k = 0;
  return <div className="viz viz-cut">
    <div className="wave">
      {segs.map(([t, n], si) => <span key={si} className={`seg ${t}`}>
        {Array.from({ length: n }, () => { k++; const h = t === "w" ? 30 + ((k * 37) % 60) : 6 + ((k * 13) % 10); return <i key={k} style={css({ "--h": `${h}%` })} />; })}
        {t === "u" && <em>um</em>}
      </span>)}
    </div>
    <div className="cut-foot"><span>Raw take 0:42</span><b>Tight cut 0:31</b></div>
  </div>;
}

// Motion graphics: a stat counts up, bars draw, a playhead scrubs.
export function Motion() {
  return <div className="viz viz-motion">
    <div className="m-stage">
      <span className="m-label">Members this year</span>
      <span className="m-num" />
      <div className="m-bars">{[34, 48, 41, 62, 77, 100].map((h, i) => <span key={i} style={css({ "--h": `${h}%`, "--i": i })} />)}</div>
    </div>
    <div className="m-track"><span className="m-head" /></div>
  </div>;
}
