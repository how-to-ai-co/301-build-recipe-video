---
name: yap-cover-image
description: Create and attach a finished 9:16 cover image with every completed video edit in this video engine, especially Yap talking-head videos. Use for video thumbnails, cover revisions, and final video delivery.
---

# Yap Cover Image

A cover is a separate still that represents the video before playback. In this video engine, every completed video delivery includes a cover, unless the user explicitly opts out. Do not stop at suggesting one. Produce a first design using judgment, then invite feedback through the delivered result. This requirement does not authorize posting, uploading, or altering the video itself.

Before starting, read the cover notes in `recipes/yap.md` and `.claude/skills/video-edit/references/edit-rules.md`. Where the recipe gives a newer cover rule (for example, using the most impressive frame of the opening visual hook), the recipe wins.

## Choose the frame and concept

Inspect a contact sheet of several moments from the approved edit, then inspect promising candidates at full resolution. Select sharp eyes, a natural engaging expression, good lighting, and an intentional-looking gesture. Avoid blinks, motion blur, awkward mouth shapes, hands blocking the face, and partially entered or faded graphics. Choose deliberately; do not default to the first frame or a random timestamp. Record the chosen edited timestamp and corresponding source time when a verified cut map is available.

Represent the video's central idea, not a passing reference. Reuse an approved composed frame when it already makes a strong cover. Otherwise use the selected presenter frame with a small number of relevant approved assets. A cover is a single visual promise, not a collage of every overlay. Use authentic product artwork or screenshots for identifiable products. Do not invent results or revive rejected visuals. New image generation is optional and must respect the user's current preferences and tool requirements; cover creation does not inherently require generation.

Use a short, readable Title Case headline. Start with the approved video title; shorten or strengthen only when justified by the content. Preserve acronyms. Use the video's visual language, but judge it as a still at thumbnail size. Aim for one clear hierarchy: face, headline, supporting image. Avoid tiny interface text and decorative clutter. Keep text editable when authoring a new composition.

## Compose and review

- Default master: 1080×1920, full 9:16, exported as a separate PNG. Provide a high-quality JPG too when useful for delivery.
- Apply the Instagram safe rectangle x=35–980, y=220–1470 at 1080×1920 (see `instagram-safe-zone.md`). Keep headline, face and essential image content inside it with breathing room. Scale proportionally.
- Preserve the original presenter framing unless the user authorizes reframing. For art behind the presenter, use a matching foreground cutout at exactly the original scale and position. Do not move the presenter merely to fit art.
- Inspect the actual composition with the safe-zone exclusions overlaid, plus a small thumbnail preview. Inspect likely grid crops such as centered 3:4 and 4:5 as composition stress tests, not guarantees of the current platform interface. If an exact current platform crop is required, verify it. Keep the headline and face intact in the intended crop; adapt cover layout independently if necessary without changing the approved video.
- Inspect the final exported image, not just the working canvas. Reject blur, clipped text, unreadable type, weak expression, incomplete overlay transitions, or broken masking. Keep review guides out of the delivered master.

Use the project's existing tools for composition and export. An approved composed video frame can be extracted losslessly to PNG with ffmpeg. Keep original media and final video unchanged.

## Deliver with the video

Save beside the final video with a matching versioned name, e.g. `Video-v10-cover.png`. Display the actual cover inline in the final chat alongside the playable video and give the file path. Retain a reproducible source: chosen timestamp/frame number and source project, or a separate editable cover composition when changed. Do not describe a cover as attached unless the image is actually included in the response.

For a cover-only request, deliver the image inline without rerendering or reposting the video. On later video revisions, verify that the existing cover remains accurate; refresh it if title, visual style or subject changes, and include the matching cover again at completion.

When the user gives feedback on a cover, use the `refine-video-edit` skill to save any reusable rule.
