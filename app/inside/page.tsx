import type { CSSProperties } from "react";
import type { Metadata } from "next";
import { ArrowUpRight, Check } from "lucide-react";
import { REPO, headliners, packs, notIncluded, totalFeatures, repoLink, tree } from "@/content/inside";
import { Topbar } from "../topbar";
import { PackIcon } from "../icons";

export const metadata: Metadata = {
  title: "What's inside | 301 Build Recipe: Video | How to AI",
  description: `${totalFeatures} free video tools in ${packs.length} packs: an editor that learns your taste, make-mine-like-this, a talking-head editor and a motion graphics studio.`,
};

const tone = (t: string) => ({ "--tone": `var(--t-${t})`, "--tint": `var(--t-${t}-tint)` }) as CSSProperties;
const costLabel = { free: "Free", paid: "Pay as you go", mac: "Mac" } as const;

export default function Inside() {
  const skills = packs.find(p => p.id === "skills")!.features.length;
  return <>
    <div className="wrap"><Topbar active="inside" /></div>

    <header className="showcase-hero">
      <div className="wrap-inner">
        <span className="pill-free">Free with AI 301</span>
        <h1>Everything you get.</h1>
        <p>{totalFeatures} features in {packs.length} packs, in one folder you keep. Clone it once and Claude can reach for any of it. Most of it needs no account and no API key.</p>
        <ul className="hero-stats">
          <li><b>{packs.length}</b><span>packs</span></li>
          <li><b>{totalFeatures}</b><span>features</span></li>
          <li><b>{skills}</b><span>smart skills</span></li>
          <li><b>$0</b><span>to start</span></li>
        </ul>
        <div className="hero-cta">
          <a className="btn" href="./">Get the prompt</a>
          <a className="btn btn-ghost" href={REPO} target="_blank" rel="noreferrer"><img src="/logos/github.svg" alt="" width={16} height={16} className="invert" /> Open on GitHub</a>
        </div>
      </div>
    </header>

    <div className="wrap">
      <section className="headliners" aria-labelledby="hl">
        <span className="eyebrow accent">The headliners</span>
        <h2 id="hl" className="sec-title">Four things you&apos;ll use every week</h2>
        <div className="hl-grid">
          {headliners.map(h => <a key={h.title} className="hl" href={repoLink(h.path)} target="_blank" rel="noreferrer" style={tone(h.tone)}>
            <span className="tile big"><PackIcon name={h.icon} size={28} /></span>
            <h3>{h.title}</h3>
            <p>{h.pitch}</p>
            <ul>{h.gets.map(g => <li key={g}><Check size={15} aria-hidden="true" />{g}</li>)}</ul>
          </a>)}
        </div>
      </section>

      <section aria-labelledby="packs">
        <span className="eyebrow accent">The packs</span>
        <h2 id="packs" className="sec-title">All {totalFeatures} features</h2>
        <nav className="pack-nav" aria-label="Packs">
          {packs.map(p => <a key={p.id} href={`#${p.id}`} style={tone(p.tone)}><span className="tile sm"><PackIcon name={p.icon} size={15} /></span>{p.name}<em>{p.features.length}</em></a>)}
        </nav>

        <div className="packs">
          {packs.map(p => <article key={p.id} id={p.id} className="pack" style={tone(p.tone)}>
            <header className="pack-head">
              <span className="tile"><PackIcon name={p.icon} /></span>
              <div>
                <h3>{p.name}</h3>
                <p>{p.tagline}</p>
              </div>
              <span className="pack-count">{p.features.length} features</span>
            </header>
            <ul className="feats">
              {p.features.map(f => <li key={f.title}>
                <a href={repoLink(f.path)} target="_blank" rel="noreferrer">
                  <Check size={16} className="tick" aria-hidden="true" />
                  <span className="feat-body">
                    <span className="feat-top"><b>{f.title}</b>{f.cost && f.cost !== "free" && <em className={`cost ${f.cost}`}>{costLabel[f.cost]}</em>}</span>
                    <span className="feat-what">{f.what}</span>
                  </span>
                </a>
              </li>)}
            </ul>
            <a className="pack-open" href={tree(p.folder)} target="_blank" rel="noreferrer">Open the {p.name} on GitHub <ArrowUpRight size={14} aria-hidden="true" /></a>
          </article>)}
        </div>
      </section>

      <section className="closer">
        <h2>Ready to use it?</h2>
        <p>Copy the prompt, paste it into Claude Code, and Claude sets all of this up for you.</p>
        <a className="btn" href="./">Get the prompt</a>
        <details className="fine">
          <summary>What&apos;s not included</summary>
          <ul>{notIncluded.map(n => <li key={n}>{n}</li>)}</ul>
        </details>
      </section>
    </div>
    <footer className="foot">How to AI · AI 301</footer>
  </>;
}
