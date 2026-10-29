"use client";
import { useRef, useState } from "react";
import { Check, Copy, Download, FileText } from "lucide-react";

function fallbackCopy(text: string) {
  const t = document.createElement("textarea"); t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
  document.body.appendChild(t); t.select(); const ok = document.execCommand("copy"); t.remove(); return ok;
}

export function CopyPrompt({ text, lines }: { text: string; lines: number }) {
  const [state, setState] = useState<"idle" | "copied" | "error">("idle");
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);
  async function copy() {
    let ok = false;
    try { await navigator.clipboard.writeText(text); ok = true; } catch { ok = fallbackCopy(text); }
    setState(ok ? "copied" : "error"); clearTimeout(timer.current); timer.current = setTimeout(() => setState("idle"), ok ? 2500 : 6000);
  }
  return (
    <div className="prompt">
      <div className="prompt-file">
        <FileText size={20} aria-hidden="true" />
        <div><b>301-video-recipe.md</b><span>{lines} lines · paste it into Claude Code</span></div>
      </div>
      <div className="prompt-actions">
        <a className="btn btn-secondary" href="build-recipe.md" download="301-video-recipe.md"><Download size={16} aria-hidden="true" /> Download</a>
        <button className="btn" onClick={copy}>{state === "copied" ? <Check size={16} aria-hidden="true" /> : <Copy size={16} aria-hidden="true" />}{state === "copied" ? "Copied" : "Copy prompt"}</button>
      </div>
      <p aria-live="polite" className="prompt-status">
        {state === "copied" && "Copied. Paste it into a new Claude Code session."}
        {state === "error" && "Your browser blocked copying. Use Download instead."}
      </p>
    </div>
  );
}
