import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * Yap overlay: software "bundling" into one chat box (mode="bundle"), or bursting
 * back out of it (mode="unbundle"). Timed to speech: each logo appears on its own
 * frame (`appear`), and the move into / out of the box starts at `moveAt`.
 * Rendered with alpha and composited over the talking head, inside the Instagram
 * safe area (x 35-980, y 220-1470 at 1080x1920) and above the eyes.
 */
export type BundleProps = { mode: "bundle" | "unbundle"; logos: string[]; appear: number[]; moveAt: number; duration: number };

const PANEL = { x: 110, y: 450, w: 860, h: 470 };
const BOX = { w: 620, h: 96, cy: PANEL.y + PANEL.h / 2 + 10 };
const SPOTS = [
  { x: 250, y: 560 }, { x: 830, y: 560 }, { x: 250, y: 830 }, { x: 830, y: 830 }, { x: 540, y: 530 },
];

export const Bundle: React.FC<BundleProps> = ({ mode, logos, appear, moveAt }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const fadeOut = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], { extrapolateLeft: "clamp" });
  const panelIn = spring({ frame, fps, config: { damping: 18 } });
  const travel = spring({ frame: frame - moveAt, fps, config: { damping: 20, mass: 1.2 } });
  // p = 0: apps spread out; p = 1: inside the chat box.
  const p = mode === "bundle" ? travel : 1 - travel;
  const boxPulse = interpolate(p, [0.85, 1], [1, 1.06], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <div style={{
        position: "absolute", left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, borderRadius: 34,
        background: "rgba(10,10,12,0.78)", transform: `scale(${0.92 + 0.08 * panelIn})`, opacity: panelIn,
      }} />
      <div style={{
        position: "absolute", left: 540 - BOX.w / 2, top: BOX.cy - BOX.h / 2, width: BOX.w, height: BOX.h, borderRadius: 48,
        background: "white", display: "flex", alignItems: "center", padding: "0 18px 0 38px", boxSizing: "border-box",
        transform: `scale(${boxPulse * (0.9 + 0.1 * panelIn)})`, opacity: panelIn,
        boxShadow: `0 0 ${44 * p}px rgba(255,255,255,${0.55 * p})`,
        fontFamily: "-apple-system, 'SF Pro Display', sans-serif",
      }}>
        <span style={{ flex: 1, fontSize: 40, color: "#8e8e93" }}>Ask anything</span>
        <div style={{ width: 64, height: 64, borderRadius: 32, background: "#111", color: "white", fontSize: 38,
          display: "flex", alignItems: "center", justifyContent: "center" }}>↑</div>
      </div>
      {logos.map((src, i) => {
        const s = SPOTS[i % SPOTS.length];
        // Bundle: each logo pops in when it is named. Unbundle: they burst out together at moveAt.
        const pop = mode === "bundle" ? spring({ frame: frame - (appear[i] ?? 0), fps, config: { damping: 12 } }) : 1;
        const x = interpolate(p, [0, 1], [s.x, 540]);
        const y = interpolate(p, [0, 1], [s.y, BOX.cy]);
        const scale = interpolate(p, [0, 1], [1, 0.12]) * pop;
        const opacity = interpolate(p, [0.75, 1], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) * panelIn * Math.min(1, pop * 2);
        return (
          <div key={src} style={{
            position: "absolute", left: x - 75, top: y - 75, width: 150, height: 150, borderRadius: 32, background: "white",
            display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${scale})`, opacity,
          }}>
            <Img src={staticFile(src)} style={{ width: 112, height: 112, objectFit: "contain" }} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
