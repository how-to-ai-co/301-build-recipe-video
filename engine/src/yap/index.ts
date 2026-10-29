import React from "react";
import { Composition, registerRoot } from "remotion";
import { Bundle } from "./Bundle";

// Yap overlays live in their own entry point so they never touch the ad compositions in Root.tsx.
// Render with alpha (yap.py's Yap.remotion() builds this command):
//   npx remotion render src/yap/index.ts Bundle out.mov --codec=prores --prores-profile=4444 \
//     --pixel-format=yuva444p10le --image-format=png --props='{"mode":"bundle","logos":[...],"appear":[...],"moveAt":90,"duration":150}'
const YapRoot: React.FC = () =>
  React.createElement(Composition, {
    id: "Bundle", component: Bundle as any, width: 1080, height: 1920, fps: 30, durationInFrames: 96,
    defaultProps: { mode: "bundle", logos: [], appear: [], moveAt: 32, duration: 96 },
    calculateMetadata: ({ props }: any) => ({ durationInFrames: props.duration }),
  });

registerRoot(YapRoot);
