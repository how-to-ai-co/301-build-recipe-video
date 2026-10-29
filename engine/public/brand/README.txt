Brand assets go here, all optional:
  - avatar PNG and wordmark PNGs, wired through src/brand.mjs
  - logo SVGs for the paid offer wall (see TOOLS in src/AdCaptions.tsx)
  - a .ttf/.otf for the aerial lockup: scripts/render_aerial.py picks up the
    first font file in this folder automatically, system font otherwise

The Remotion formats use system font stacks on purpose (no font loading, no
licence, no FOUT) — a font here only affects the aerial format.
