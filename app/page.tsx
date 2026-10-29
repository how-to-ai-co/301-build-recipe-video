import type { CSSProperties } from "react";
import { ArrowUpRight } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { REPO, prompt, headliners, packs, totalFeatures } from "@/content/inside";
import { PackIcon } from "./icons";
import { Topbar } from "./topbar";
import recipe from "@/content/recipe.json";
import { CopyPrompt } from "./copy-prompt";
import { Bring, Study, Plan, Draft, Learn } from "./viz";

const lines = (recipe as string).trimEnd().split("\n").length;
const css = (v: Record<string, string | number>) => v as CSSProperties;

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
      <Topbar active="steps" />

      <header className="hero">
        <div className="course-tag"><span className="course-num">AI 301</span><span>Live course · Video</span></div>
        <h1>Your video, made.</h1>
        <CopyPrompt text={recipe as string} lines={lines} />
        <a className="repo-link" href={REPO} target="_blank" rel="noreferrer"><img src="/logos/github.svg" alt="" width={16} height={16} /> github.com/how-to-ai-co/301-build-recipe-video <ArrowUpRight size={14} aria-hidden="true" /></a>
        <a className="teaser" href="inside">
          <span className="teaser-icons">{headliners.map(h => <span key={h.title} className="tile sm" style={css({ "--tone": `var(--t-${h.tone})`, "--tint": `var(--t-${h.tone}-tint)` })}><PackIcon name={h.icon} size={15} /></span>)}</span>
          <span><b>Plus {totalFeatures} free features inside.</b> An editor that learns your taste, make-mine-like-this, a motion studio and more.</span>
          <ArrowUpRight size={18} aria-hidden="true" />
        </a>
      </header>

      <ol className="flow-steps" aria-label="What you get">
        {steps.map((s, i) => <li key={s.t} className="step">
          <div className="step-text">
            <span className="big-num">{i + 1}</span>
            <h2>{s.t}</h2>
            <p>{s.d}</p>
            {s.link && <a className="step-link" href="inside">See everything inside <ArrowUpRight size={15} aria-hidden="true" /></a>}
          </div>
          <div aria-hidden="true">{s.v}</div>
        </li>)}
      </ol>

      <section className="gets" aria-labelledby="gets">
        <div className="gets-head">
          <span className="eyebrow accent">Included with AI 301</span>
          <h2 id="gets">What you get: {totalFeatures} features in {packs.length} packs</h2>
          <p>The prompt sets up a folder you keep. Here&apos;s what&apos;s in it.</p>
        </div>
        <div className="gets-hl">
          {headliners.map(h => <a key={h.title} href="inside" style={css({ "--tone": `var(--t-${h.tone})`, "--tint": `var(--t-${h.tone}-tint)` })}>
            <span className="tile"><PackIcon name={h.icon} /></span><b>{h.title}</b><span>{h.pitch}</span>
          </a>)}
        </div>
        <ul className="gets-packs">
          {packs.map(p => <li key={p.id}><a href={`inside#${p.id}`} style={css({ "--tone": `var(--t-${p.tone})`, "--tint": `var(--t-${p.tone}-tint)` })}>
            <span className="tile sm"><PackIcon name={p.icon} size={15} /></span>{p.name}<em>{p.features.length}</em>
          </a></li>)}
        </ul>
        <a className="btn gets-cta" href="inside">See everything inside <ArrowUpRight size={16} aria-hidden="true" /></a>
      </section>

      <section className="does" id="prompt">
        <span className="eyebrow accent">The prompt</span>
        <h2>What the prompt does</h2>
        <p className="lede">You paste it once. Claude works through eight steps, and only stops for your answers, your approvals and anything that costs money.</p>
        <ol className="does-list">
          {prompt.map((p, i) => <li key={p.t}><span className="n">{i + 1}</span><div><b>{p.t}</b><p>{p.d}</p></div></li>)}
        </ol>
        <details className="full">
          <summary>Read the full prompt</summary>
          <div className="md"><ReactMarkdown remarkPlugins={[remarkGfm]}>{recipe as string}</ReactMarkdown></div>
        </details>
              </section>
    </div>
    <footer className="foot">How to AI · AI 301</footer>
  </>;
}
