import type { Metadata } from "next";
import { ArrowUpRight } from "lucide-react";
import { REPO, blob, tree, sections, notIncluded } from "@/content/inside";
import { Topbar } from "../topbar";

export const metadata: Metadata = { title: "What's inside | 301 Build Recipe: Video | How to AI" };

const tag = { free: "Free", paid: "Costs money", mac: "Mac only" } as const;

export default function Inside() {
  const count = sections.reduce((n, s) => n + s.items.length, 0);
  return <>
    <div className="wrap">
      <Topbar active="inside" />
      <header className="hero inside-hero">
        <h1>What&apos;s inside.</h1>
        <p className="lede">Everything in the video engine, in one place: {count} skills, tools, guides and references across {sections.length} areas. The steps page is the quick way in. This is what Claude can reach for once you&apos;re there.</p>
        <a className="btn btn-secondary" href={REPO} target="_blank" rel="noreferrer"><img src="/logos/github.svg" alt="" width={16} height={16} /> Open the repo on GitHub</a>
      </header>

      <nav className="toc" aria-label="Sections">
        {sections.map(s => <a key={s.id} href={`#${s.id}`}>{s.title}</a>)}
      </nav>

      {sections.map(s => <section key={s.id} id={s.id} className="inv">
        <div className="inv-head">
          <h2>{s.title}</h2>
          {s.folder && <a className="folder" href={tree(s.folder)} target="_blank" rel="noreferrer">{s.folder}/ <ArrowUpRight size={13} aria-hidden="true" /></a>}
        </div>
        <p className="inv-intro">{s.intro}</p>
        <ul className="items">
          {s.items.map(it => <li key={it.name}>
            <a href={it.path.includes(".") && !it.path.endsWith("bin") ? blob(it.path) : tree(it.path)} target="_blank" rel="noreferrer">
              <span className="item-top"><b>{it.name}</b>{it.cost && <em className={`cost ${it.cost}`}>{tag[it.cost]}</em>}</span>
              <span className="item-what">{it.what}</span>
              <code>{it.path}</code>
            </a>
          </li>)}
        </ul>
      </section>)}

      <section className="inv">
        <div className="inv-head"><h2>Not in the repo</h2></div>
        <ul className="plain">{notIncluded.map(n => <li key={n}>{n}</li>)}</ul>
      </section>
    </div>
    <footer className="foot">How to AI · AI 301</footer>
  </>;
}
