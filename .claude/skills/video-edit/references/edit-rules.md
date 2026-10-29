# Edit rules

Your saved rules for every video edit. Claude reads this file before each plan or render, and checks each draft against it.

How it works:
- Each rule is a yes/no question about the draft. "No" means fix it before showing the draft.
- The `refine-video-edit` skill adds a rule each time you give feedback that should apply to future videos. The date and the video it came from go in brackets.
- Rules marked **(starter)** came with this folder. Delete or change any you disagree with. When you confirm one, the tag comes off.
- If two rules disagree, the newer one wins, and the older one should be removed.

## Pacing
- (starter) Is there no dead air at the start or the end of the video?
- (starter) Does something change on screen at least every few seconds, so no stretch feels stuck?
- (starter) Is the playback speed one steady value for the whole video, not jumping around?

## Text and titles
- (starter) Is every piece of on-screen text inside the Instagram safe area (see `instagram-safe-zone.md`)?
- (starter) Is every word on screen readable at phone size, for long enough to read it?
- (starter) Is all on-screen text spelled as in the script, not as the auto-transcript heard it?

## Overlays
- (starter) Does each overlay show the exact point being said at that moment, not just a word that was mentioned?
- (starter) Is every overlay sharp, with no watermark and no visible compression?
- (starter) Is the speaker's face clear of anything that must be read?

## Audio
- (starter) Is the final loudness about -14 LUFS, with true peak at or below -1.5 dBTP?
- (starter) Are there no clipped words, pops or clicks at any cut?
- (starter) Has a person listened to the final file on headphones?

## Captions
- (starter) Are captions only there if the user asked for them?
- (starter) Do captions match the spoken words exactly, and stay in time with them?

## Colour and look
- (starter) Do all the overlays in one video share one look (colours, corners, shadows)?
- (starter) Does the video match the style the user picked, if they picked one?

## Delivery
- (starter) Is the final video saved where the user asked, with a matching cover image next to it?
- (starter) Was the actual finished file checked (length, size, a few frames), not just the plan?

## One-off exceptions

Fixes for a single video do not belong here. Save those in that video's own notes (for example `output/<project>/feedback.md`). This file is only for rules that should apply to every future video.
