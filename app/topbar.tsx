import { REPO, totalFeatures } from "@/content/inside";

export function Topbar({ active }: { active: "steps" | "inside" }) {
  return <div className="topbar">
    <a href="./" className="wordmark">How to AI<span className="dot">.</span></a>
    <nav className="nav" aria-label="Pages">
      <a href="./" aria-current={active === "steps" ? "page" : undefined}>Steps</a>
      <a href="inside" className="nav-inside" aria-current={active === "inside" ? "page" : undefined}>What&apos;s inside <span className="nav-count">{totalFeatures}</span></a>
      <a href={REPO} target="_blank" rel="noreferrer" className="gh"><img src="/logos/github.svg" alt="" width={16} height={16} /> <span className="gh-label">GitHub</span></a>
    </nav>
  </div>;
}
