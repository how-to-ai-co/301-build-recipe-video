import { AudioWaveform, Brain, Clapperboard, Library, ListChecks, Mic, Paintbrush, Palette, Repeat, ScanEye, Scissors, Shapes, Smartphone, Sparkles } from "lucide-react";
import type { Icon } from "@/content/inside";

const map = { AudioWaveform, Brain, Clapperboard, Library, ListChecks, Mic, Paintbrush, Palette, Repeat, ScanEye, Scissors, Shapes, Smartphone, Sparkles };

export function PackIcon({ name, size = 22 }: { name: Icon; size?: number }) {
  const C = map[name];
  return <C size={size} strokeWidth={1.9} aria-hidden="true" />;
}
