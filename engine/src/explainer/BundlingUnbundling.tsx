import React from "react";
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * 60-second explainer: bundling and unbundling, the two ways to make money.
 * 1920x1080, 30fps. Gold, bronze and black. Text and shapes only.
 */

export const FPS = 30;
export const DURATION = 60 * FPS;

const C = {
  black: "#0B0A08",
  gold: "#D4AF37",
  goldLight: "#F1D58A",
  bronze: "#B07A3E",
  bronzeDark: "#6E4520",
  cream: "#EFE6CF",
  dim: "#8A7F6A",
};
const SERIF = "Didot, 'Bodoni 72', 'Playfair Display', Georgia, serif";
const SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif";

const ease = Easing.bezier(0.22, 1, 0.36, 1);
const ci = (f: number, a: number, b: number, o0 = 0, o1 = 1) =>
  interpolate(f, [a, b], [o0, o1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
const inOut = (f: number, start: number, end: number, fade = 15) =>
  Math.min(ci(f, start, start + fade), ci(f, end - fade, end, 1, 0));

// ---------------------------------------------------------------- shared bits

const Background: React.FC = () => {
  const f = useCurrentFrame();
  const x = 50 + 12 * Math.sin(f / 200);
  const y = 45 + 8 * Math.cos(f / 260);
  const corner = (cx: number, cy: number, dx: number, dy: number) => (
    <path
      d={`M ${cx + dx * 70} ${cy} L ${cx} ${cy} L ${cx} ${cy + dy * 70}`}
      stroke={C.bronze}
      strokeWidth={2}
      fill="none"
      opacity={0.55}
    />
  );
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at ${x}% ${y}%, #241C10 0%, ${C.black} 62%)`,
      }}
    >
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {corner(48, 48, 1, 1)}
        {corner(1872, 48, -1, 1)}
        {corner(48, 1032, 1, -1)}
        {corner(1872, 1032, -1, -1)}
      </svg>
    </AbsoluteFill>
  );
};

const Header: React.FC<{
  num: string;
  title: string;
  sub: string;
  opacity: number;
}> = ({ num, title, sub, opacity }) => (
  <div
    style={{
      position: "absolute",
      left: 140,
      top: 88,
      opacity,
      transform: `translateX(${(1 - opacity) * -20}px)`,
    }}
  >
    <div style={{ display: "flex", alignItems: "baseline", gap: 26 }}>
      <span
        style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 60, color: C.gold }}
      >
        {num}
      </span>
      <span
        style={{
          fontFamily: SANS,
          fontSize: 28,
          letterSpacing: "0.42em",
          color: C.cream,
          fontWeight: 500,
        }}
      >
        {title}
      </span>
    </div>
    <div style={{ width: 120, height: 2, background: C.bronze, margin: "14px 0 16px" }} />
    <div style={{ fontFamily: SERIF, fontSize: 42, color: C.cream, opacity: 0.92 }}>
      {sub}
    </div>
  </div>
);

const Caption: React.FC<{
  f: number;
  start: number;
  end: number;
  y?: number;
  children: React.ReactNode;
}> = ({ f, start, end, y = 880, children }) => {
  const o = inOut(f, start, end, 14);
  const rise = (1 - ci(f, start, start + 20)) * 18;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
        textAlign: "center",
        opacity: o,
        transform: `translateY(${rise}px)`,
        fontFamily: SERIF,
        fontSize: 48,
        color: C.cream,
      }}
    >
      {children}
    </div>
  );
};

const Gold: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ color: C.gold, fontStyle: "italic" }}>{children}</span>
);
const Bronze: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ color: C.bronze, fontStyle: "italic" }}>{children}</span>
);

// ---------------------------------------------------------------- 1. the quote

const Quote: React.FC = () => {
  const f = useCurrentFrame();
  const out = ci(f, 192, 210, 1, 0);
  const rise = (v: number) => ({ opacity: v, transform: `translateY(${(1 - v) * 24}px)` });
  const l1 = ci(f, 12, 42);
  const l2 = ci(f, 32, 62);
  const l3 = ci(f, 72, 104);
  const attr = ci(f, 118, 146);
  return (
    <AbsoluteFill
      style={{
        opacity: out,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div style={{ width: ci(f, 0, 44, 0, 260), height: 2, background: C.gold, marginBottom: 64 }} />
      <div
        style={{
          fontFamily: SERIF,
          color: C.cream,
          fontSize: 86,
          lineHeight: 1.22,
          textAlign: "center",
        }}
      >
        <div style={rise(l1)}>“There’s only two ways I know of</div>
        <div style={rise(l2)}>to make money:</div>
        <div style={{ ...rise(l3), marginTop: 18 }}>
          <Gold>bundling</Gold> and <Bronze>unbundling.</Bronze>”
        </div>
      </div>
      <div
        style={{
          opacity: attr,
          marginTop: 64,
          fontFamily: SANS,
          letterSpacing: "0.32em",
          fontSize: 22,
          color: C.dim,
          textTransform: "uppercase",
        }}
      >
        Jim Barksdale · former CEO of Netscape
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------ 2. the newspaper, bundled then unbundled

const TW = 270;
const TH = 110;
const TILES = [
  { label: "News", to: "News sites" },
  { label: "Sports", to: "ESPN" },
  { label: "Weather", to: "Weather apps" },
  { label: "Classifieds", to: "Craigslist" },
  { label: "Comics", to: "Webcomics" },
  { label: "Recipes", to: "Recipe blogs" },
];
const CLASSIFIEDS = 3;
const grid = (i: number) => ({ x: 676 + (i % 3) * 284, y: 493 + Math.floor(i / 3) * 134 });
const SCATTER = [
  { x: 360, y: 560, r: -9 },
  { x: 1580, y: 430, r: 7 },
  { x: 1220, y: 880, r: -5 },
  { x: 560, y: 870, r: 11 },
  { x: 1620, y: 720, r: -7 },
  { x: 930, y: 390, r: 5 },
];
const APART = [
  { x: 380, y: 400 },
  { x: 960, y: 400 },
  { x: 1540, y: 400 },
  { x: 380, y: 680 },
  { x: 960, y: 680 },
  { x: 1540, y: 680 },
];
const BOX = { x: 506, y: 398, w: 908, h: 324 };

const Newspaper: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sceneOut = ci(f, 820, 840, 1, 0);

  const glow = inOut(f, 270, 470, 20);
  const boxDraw = ci(f, 125, 165);
  const boxFade = ci(f, 478, 500, 1, 0);
  const perim = 2 * (BOX.w + BOX.h);

  const tiles = TILES.map((t, i) => {
    const s = SCATTER[i];
    const g = grid(i);
    const a = APART[i];
    const gather = spring({ frame: f - 72 - i * 6, fps, config: { damping: 16, mass: 0.8 } });
    const split = spring({ frame: f - 492 - i * 4, fps, config: { damping: 13, mass: 0.9 } });
    const bob = (1 - gather) * Math.sin(f / 18 + i * 1.7) * 7;
    let x = s.x + (g.x - s.x) * gather;
    let y = s.y + (g.y - s.y) * gather + bob;
    x += (a.x - g.x) * split;
    y += (a.y - g.y) * split;
    const rot = s.r * (1 - gather);
    const appear = ci(f, 14 + i * 5, 36 + i * 5);
    const isCl = i === CLASSIFIEDS;
    const hl = isCl ? glow : 0;
    // After the split, every piece stands on its own: gold edge for all.
    const solo = ci(f, 520 + i * 6, 550 + i * 6);
    const edge = hl > 0 || solo > 0.5 ? C.gold : C.bronze;
    const subOpacity = ci(f, 530 + i * 8, 556 + i * 8);
    return (
      <React.Fragment key={t.label}>
        <div
          style={{
            position: "absolute",
            left: x - TW / 2,
            top: y - TH / 2,
            width: TW,
            height: TH,
            opacity: appear,
            transform: `rotate(${rot}deg) scale(${1 + 0.06 * hl})`,
            border: `2px solid ${edge}`,
            background: `linear-gradient(160deg, ${
              hl > 0 ? "#3A2C10" : "#1D170E"
            }, #0F0C08)`,
            boxShadow: `0 0 ${50 * hl}px rgba(212,175,55,${0.55 * hl})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: SERIF,
            fontSize: 42,
            color: hl > 0.3 ? C.goldLight : C.cream,
            zIndex: isCl ? 2 : 1,
          }}
        >
          {t.label}
        </div>
        <div
          style={{
            position: "absolute",
            left: a.x - 200,
            width: 400,
            top: a.y + TH / 2 + 12,
            textAlign: "center",
            opacity: subOpacity,
            fontFamily: SERIF,
            fontStyle: "italic",
            fontSize: 36,
            color: C.gold,
          }}
        >
          → {t.to}
        </div>
      </React.Fragment>
    );
  });

  // Money flowing out of the classifieds into every other section.
  const coins: React.ReactNode[] = [];
  const tMoney = f - 290;
  const moneyOn = inOut(f, 290, 468, 15);
  if (tMoney >= 0 && moneyOn > 0) {
    const from = grid(CLASSIFIEDS);
    TILES.forEach((_, j) => {
      if (j === CLASSIFIEDS) return;
      const to = grid(j);
      for (let k = 0; k < 3; k++) {
        const p = ((tMoney + k * 16 + j * 7) % 48) / 48;
        const x = from.x + (to.x - from.x) * p;
        const y = from.y + (to.y - from.y) * p - Math.sin(Math.PI * p) * 60;
        coins.push(
          <div
            key={`${j}-${k}`}
            style={{
              position: "absolute",
              left: x - 14,
              top: y - 22,
              fontFamily: SANS,
              fontWeight: 700,
              fontSize: 34,
              color: C.goldLight,
              opacity: Math.sin(Math.PI * p) * moneyOn,
              textShadow: `0 0 12px ${C.gold}`,
              zIndex: 3,
            }}
          >
            $
          </div>
        );
      }
    });
  }

  return (
    <AbsoluteFill style={{ opacity: sceneOut }}>
      <Header
        num="01"
        title="BUNDLING"
        sub="Take separate things and sell them as one."
        opacity={inOut(f, 0, 468, 18)}
      />
      <Header
        num="02"
        title="UNBUNDLING"
        sub="Pull out one piece, do it better, sell it on its own."
        opacity={inOut(f, 474, 840, 18)}
      />

      <svg width={1920} height={1080} style={{ position: "absolute", opacity: boxFade }}>
        <rect
          x={BOX.x}
          y={BOX.y}
          width={BOX.w}
          height={BOX.h}
          fill="rgba(212,175,55,0.04)"
          stroke={C.gold}
          strokeWidth={2.5}
          strokeDasharray={perim}
          strokeDashoffset={perim * (1 - boxDraw)}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: BOX.y - 50,
          textAlign: "center",
          opacity: ci(f, 140, 168) * boxFade,
          fontFamily: SANS,
          fontSize: 24,
          letterSpacing: "0.5em",
          color: C.gold,
        }}
      >
        THE NEWSPAPER
      </div>

      {tiles}
      {coins}

      <Caption f={f} start={172} end={272}>
        One price. One place. One daily habit.
      </Caption>
      <Caption f={f} start={290} end={378}>
        The secret: <Gold>classified ads</Gold> made the money…
      </Caption>
      <Caption f={f} start={378} end={468}>
        …and that money paid for everything else.
      </Caption>
      <Caption f={f} start={570} end={690} y={850}>
        Online, each piece was done better — often for free.
      </Caption>
      <Caption f={f} start={696} end={832} y={850}>
        Lose the <Gold>classifieds</Gold>, and the bundle loses its money.
      </Caption>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 3. the cycle

const COLS = [
  { x: 640, title: "BUNDLE", color: C.gold },
  { x: 1090, title: "UNBUNDLE", color: C.bronze },
  { x: 1540, title: "REBUNDLE", color: C.gold },
];
const ROWS = [
  { y: 510, label: "MUSIC", cells: ["The album", "The 99¢ single", "Spotify"], at: 70 },
  { y: 680, label: "TV", cells: ["Cable TV", "Netflix · HBO · Disney+", "Streaming bundles"], at: 175 },
];
const CW = 390;
const CH = 108;

const Cycle: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sceneOut = ci(f, 430, 450, 1, 0);
  const arcDraw = ci(f, 285, 345);
  const arcLen = 1100;

  return (
    <AbsoluteFill style={{ opacity: sceneOut }}>
      <Header
        num="03"
        title="THE CYCLE"
        sub="Every bundle gets unbundled. Then it gets rebundled."
        opacity={inOut(f, 0, 450, 18)}
      />

      {COLS.map((c, i) => {
        const o = ci(f, 22 + i * 10, 48 + i * 10);
        return (
          <div
            key={c.title}
            style={{
              position: "absolute",
              left: c.x - 200,
              width: 400,
              top: 370,
              textAlign: "center",
              opacity: o,
              fontFamily: SANS,
              fontSize: 26,
              letterSpacing: "0.42em",
              color: c.color,
              fontWeight: 600,
            }}
          >
            {c.title}
          </div>
        );
      })}

      {ROWS.map((r) => (
        <React.Fragment key={r.label}>
          <div
            style={{
              position: "absolute",
              left: 140,
              top: r.y - 16,
              opacity: ci(f, r.at - 10, r.at + 12),
              fontFamily: SANS,
              fontSize: 24,
              letterSpacing: "0.35em",
              color: C.dim,
            }}
          >
            {r.label}
          </div>
          {r.cells.map((txt, i) => {
            const start = r.at + i * 35;
            const s = spring({ frame: f - start, fps, config: { damping: 15 } });
            const col = COLS[i];
            return (
              <div
                key={txt}
                style={{
                  position: "absolute",
                  left: col.x - CW / 2,
                  top: r.y - CH / 2,
                  width: CW,
                  height: CH,
                  opacity: Math.min(1, s * 1.4),
                  transform: `translateY(${(1 - s) * 30}px)`,
                  border: `2px solid ${col.color}`,
                  background: "linear-gradient(160deg, #1D170E, #0F0C08)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: SERIF,
                  fontSize: txt.length > 18 ? 32 : 40,
                  color: C.cream,
                }}
              >
                {txt}
              </div>
            );
          })}
        </React.Fragment>
      ))}

      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <marker id="head" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill={C.goldLight} />
          </marker>
        </defs>
        {ROWS.flatMap((r) =>
          [0, 1].map((i) => {
            const d = ci(f, r.at + i * 35 + 18, r.at + i * 35 + 34);
            const x1 = COLS[i].x + CW / 2 + 10;
            const x2 = COLS[i + 1].x - CW / 2 - 14;
            return (
              <line
                key={`${r.label}-${i}`}
                x1={x1}
                y1={r.y}
                x2={x1 + (x2 - x1) * d}
                y2={r.y}
                stroke={C.goldLight}
                strokeWidth={2.5}
                opacity={d}
                markerEnd={d > 0.95 ? "url(#head)" : undefined}
              />
            );
          })
        )}
        {/* around again: rebundle back to bundle */}
        <path
          d={`M ${COLS[2].x} ${680 + CH / 2 + 12} C ${COLS[2].x} 860, ${COLS[0].x} 860, ${COLS[0].x} ${
            680 + CH / 2 + 16
          }`}
          stroke={C.bronze}
          strokeWidth={2.5}
          fill="none"
          strokeDasharray={arcLen}
          strokeDashoffset={arcLen * (1 - arcDraw)}
          markerEnd={arcDraw > 0.97 ? "url(#head)" : undefined}
        />
      </svg>

      <Caption f={f} start={330} end={432} y={880}>
        …and around again. <Gold>Money is made at every turn.</Gold>
      </Caption>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 4. the two ways

const Card: React.FC<{
  x: number;
  start: number;
  word: string;
  color: string;
  lines: string[];
  when: string;
}> = ({ x, start, word, color, lines, when }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f - start, fps, config: { damping: 16 } });
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: 250,
        width: 600,
        height: 470,
        opacity: Math.min(1, s * 1.3),
        transform: `translateY(${(1 - s) * 40}px)`,
        border: `2px solid ${color}`,
        background: "linear-gradient(165deg, #211A0F, #0D0B07)",
        boxShadow: `0 0 60px rgba(212,175,55,0.08)`,
        padding: "48px 56px",
        boxSizing: "border-box",
      }}
    >
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 96, color, lineHeight: 1 }}>
        {word}
      </div>
      <div style={{ width: 90, height: 2, background: color, margin: "28px 0 30px" }} />
      {lines.map((l) => (
        <div key={l} style={{ fontFamily: SERIF, fontSize: 44, color: C.cream, lineHeight: 1.35 }}>
          {l}
        </div>
      ))}
      <div
        style={{
          position: "absolute",
          bottom: 44,
          left: 56,
          fontFamily: SANS,
          fontSize: 20,
          letterSpacing: "0.3em",
          color: C.dim,
        }}
      >
        {when}
      </div>
    </div>
  );
};

const TwoWays: React.FC = () => {
  const f = useCurrentFrame();
  const fadeToBlack = ci(f, 272, 300, 1, 0);
  const t = ci(f, 0, 24);
  return (
    <AbsoluteFill style={{ opacity: fadeToBlack }}>
      <div
        style={{
          position: "absolute",
          top: 118,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 30,
          opacity: t,
        }}
      >
        <div style={{ width: 140 * t, height: 2, background: C.bronze }} />
        <div
          style={{
            fontFamily: SANS,
            fontSize: 30,
            letterSpacing: "0.42em",
            color: C.gold,
            fontWeight: 500,
          }}
        >
          THE TWO WAYS TO MAKE MONEY
        </div>
        <div style={{ width: 140 * t, height: 2, background: C.bronze }} />
      </div>

      <Card
        x={330}
        start={18}
        word="Bundle"
        color={C.gold}
        lines={["Gather what’s scattered.", "Sell convenience."]}
        when="WHEN A MARKET IS FRAGMENTED"
      />
      <div
        style={{
          position: "absolute",
          left: 930,
          width: 60,
          top: 455,
          textAlign: "center",
          fontFamily: SERIF,
          fontStyle: "italic",
          fontSize: 44,
          color: C.dim,
          opacity: ci(f, 40, 60),
        }}
      >
        or
      </div>
      <Card
        x={990}
        start={48}
        word="Unbundle"
        color={C.bronze}
        lines={["Break off the best piece.", "Sell focus."]}
        when="WHEN A BUNDLE IS BLOATED"
      />

      <Caption f={f} start={140} end={320} y={800}>
        Look at any market and ask: is it <Gold>scattered</Gold> — or{" "}
        <Bronze>bloated?</Bronze>
      </Caption>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- the film

export const BundlingUnbundling: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Background />
    <Sequence from={0} durationInFrames={210}>
      <Quote />
    </Sequence>
    <Sequence from={210} durationInFrames={840}>
      <Newspaper />
    </Sequence>
    <Sequence from={1050} durationInFrames={450}>
      <Cycle />
    </Sequence>
    <Sequence from={1500} durationInFrames={300}>
      <TwoWays />
    </Sequence>
  </AbsoluteFill>
);
