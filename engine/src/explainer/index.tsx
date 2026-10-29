import React from "react";
import { Composition, registerRoot } from "remotion";
import { BundlingUnbundling, DURATION, FPS } from "./BundlingUnbundling";

const ExplainerRoot: React.FC = () => (
  <Composition
    id="BundlingUnbundling"
    component={BundlingUnbundling}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
  />
);

registerRoot(ExplainerRoot);
