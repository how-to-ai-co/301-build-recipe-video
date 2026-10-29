import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "301 Build Recipe: Video | How to AI",
  description: "Make a video for your business with Claude: talking-head edits, captions, motion graphics, and edits that learn your taste. Copy the live workshop recipe.",
  metadataBase: new URL("https://301-build-recipe-video.vercel.app"),
  robots: { index: false },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet" />
      </head>
      <body>{children}</body>
    </html>
  );
}
