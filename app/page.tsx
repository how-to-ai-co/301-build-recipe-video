import type { CSSProperties } from "react";
import { ArrowUpRight } from "lucide-react";
import recipe from "@/content/recipe.json";
import { CopyPrompt } from "./copy-prompt";

const lines = (recipe as string).trimEnd().split("\n").length;
const css = (v: Record<string, string | number>) => v as CSSProperties;
const REPO = "https://github.com/how-to-ai-co/301-build-recipe-video";

function Bring() {
  return <div className="viz viz-bring">
    <ul className="chips">
      {["instagram.com/reel/…", "IMG_4021.MOV", "yoursite.com"].map((c, i) => <li key={c} className="chip" style={css({ "--i": i })}><i />{c}</li>)}
    </ul>
    <div className="phone"><span className="glow" /></div>
  </div>;
}

function Study() {
  return <div className="viz viz-study">
    <div className="sheet">{Array.from({ length: 18 }, (_, i) => <span key={i} style={css({ "--i": i })} />)}</div>
    <div className="stats"><b>0.9s per shot</b><b>3-word hook</b><b>captions synced</b></div>
  </div>;
}

function Plan() {
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

function Draft() {
  return <div className="viz viz-draft">
    <div className="frame"><span className="title">USE AI</span><span className="cap">here&apos;s what <b>works</b></span></div>
    <ul className="checks">
      {["Hook in 1 second", "Text in safe zone", "Loudness −14 LUFS"].map((c, i) => <li key={c} style={css({ "--i": i })}>{c}</li>)}
    </ul>
  </div>;
}

function Learn() {
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

const steps = [
  { t: "Bring your footage or a link", d: "Your clip, your site, or a video you love.", v: <Bring /> },
  { t: "Claude studies the style", d: "Pacing, hook, text and look, measured.", v: <Study /> },
  { t: "Plan the edit together", d: "Every line, cut and overlay, before a render.", v: <Plan /> },
  { t: "Get a draft it already checked", d: "Claude watches its own frames first.", v: <Draft /> },
  { t: "Your notes become rules", d: "Every video starts closer to your taste.", v: <Learn />, link: true },
];

export default function Page() {
  return <>
    <div className="wrap">
      <div className="topbar"><span className="wordmark">How to AI<span className="dot">.</span></span><span className="eyebrow">AI 301 · Video</span></div>

      <header className="hero">
        <h1>Your video, made.</h1>
        <CopyPrompt text={recipe as string} lines={lines} />
      </header>

      <ol className="flow-steps" aria-label="What you get">
        {steps.map((s, i) => <li key={s.t} className="step">
          <div className="step-text">
            <span className="big-num">{i + 1}</span>
            <h2>{s.t}</h2>
            <p>{s.d}</p>
            {s.link && <a className="step-link" href={REPO} target="_blank" rel="noreferrer">See the video engine <ArrowUpRight size={15} aria-hidden="true" /></a>}
          </div>
          <div aria-hidden="true">{s.v}</div>
        </li>)}
      </ol>
    </div>
    <footer className="foot">How to AI · AI 301</footer>
  </>;
}
