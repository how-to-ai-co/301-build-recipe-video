# Video review inside Codex

Open http://127.0.0.1:8766 in a Codex browser panel. Start/restart locally with `./review-panel/start.sh` from the workspace. This uses Python's standard library and binds only to 127.0.0.1. No external account, upload, or app installation is required. The server remains running while its process is alive; after a computer restart run the start script again.

## Review

Drafts under output/ are discovered every eight seconds. Technical intermediates, source assets, masks, proxies, version archives and test renders are excluded. Related version folders are grouped; latest numbered revision is preferred over older draft copies. Older versions remain selectable. A newly rendered revision reopens the project in the review queue. An existing playhead or unsent note isn't interrupted by background refresh.

Pause, pin a timestamp, write a note and click Add note. To mark a range, pin its beginning, seek and click Mark range end. Click a saved timestamp to seek. Resolve/reopen and edit notes inline. Notes are stored atomically in review-panel/notes.json with the exact video fingerprint, path, project, timestamp and optional end. This is the file the agent should read before revisions. Times refer to the reviewed edited output, not raw source footage. Show other versions to see prior feedback; timings across revised cuts can change and require mapping.

Approve video removes the latest draft's project from In review and places it in Approved. Return to review reverses this. Approval never deletes videos or notes. Approving an older version or a scene check does not approve the latest full draft. No historical drafts were assumed approved when building the panel.

## Scene revision workflow

1. Read notes.json; identify exact reviewed version and requested interval. Follow workspace editorial rules and preserve accepted footage/audio for visual-only revisions.
2. Revise the editable source project. Save a new revision; do not modify original media.
3. Render only the affected scene plus enough surrounding context to check the entrance/exit. Use scene previews for review before a continuous final export.
4. Register the scene check under the same project with its full-output starting offset. The panel displays full-video timestamps even when the clip starts at zero. Resolve feedback only after the requested fix is implemented; visual approval belongs to the user.
5. After approval render the final full video when required. This panel is a review interface, not a live Tesseract/Remotion timeline and does not automatically apply notes or launch renders.

### Tesseract visual scene checks

From the workspace after activation:

```sh
python review-panel/scene_preview.py /absolute/path/Project.tsrct --start 12 --end 17 --group my-project --name 'Scene 2 revision'
```

The helper copies the project into output/scene-previews/, uses native grouping to preserve original clocks, limits the solo export to the selected window, and registers the preview. The original project is untouched. These solo exports are **silent visual spot-checks**: do not use them to judge audio joins or sync. The editable copied project, embedded source assets, review registration and rendered preview stay together. Validated with a moving graphic at a nonzero start against the full project's corresponding frame. Complex project effects and mattes still need composed-frame review.

Remotion can render a frame interval using its --frames option. Preserve the composition clock and register the output offset; verify audio when the revision touches sound. Stitching separately rendered chunks is an optional later optimization, not implemented by this panel.

### Explicit registration

For an excluded draft or scene preview, POST JSON to /api/register:

```json
{"path":"output/project/scene-check.mp4","group":"project","label":"Scene 2 placement","offset":12,"clip":true}
```

Use clip:false and offset:0 for a full draft. Existing project IDs are in GET /api/state. Registration is local only. Files must be inside output/.

## Verification

`python review-panel/test_review.py` uses an isolated temporary state file. It checks persisted note ranges, resolution/deletion, reversible approval, media Range requests for seeking, clip offsets, origin rejection and path containment. UI was checked in Codex's in-app browser for note persistence after reload, resolving, approval. Restoration was checked through the API. Browser playback of the existing Muse draft was inspected.

## Timestamped script

The main panel shows the entire edited script in a three-column chart: Script · output time, Edit, Overlay. Word-level transcript data is grouped into short passages without dropping wording. Click a timestamp to seek and pin that passage's start/end; notes retain its script text. Follow playhead highlights the active passage. Original source timestamps are shown when a saved cut map is available. Source time spans may cross cuts; output timestamps are the review clock.

Saved transcript mappings for specific videos can be added to `CONFIG` in `script_data.py`.

Other drafts can use Create timestamped script to transcribe the exact video locally with the cached Whisper small model. This does not render or modify the video. Automatic wording is labeled for verification, especially names. Newly authored videos should supply a `.review-script.json` sidecar beside the video with `{ "status": "ready", "rows": [{ "start": 0, "end": 2, "text": "Spoken passage", "edit": "Retained", "overlay": "Clean footage" }], "plan": [], "provenance": "Reviewed script" }`. Generate this alongside the render so its script appears immediately, using output times and optional source_start/source_end.

## Current workflow — supersedes note-taking instructions above

Request edits directly in the Claude chat, referring to the video and output timestamp. The panel displays video, cover and timestamped script; there is no note composer or browser prompt dialog. Click script timestamps to seek, then type instructions in the chat. Use the Video/Cover buttons to inspect both deliverables.

New drafts appear automatically.

Approve & Save Final validates a full video and its matching cover, stages copies, then publishes the pair in a version-specific folder under `~/Desktop/Final Content` (change the folder in `server.py` if you want it elsewhere). Approval is recorded only after copying succeeds. Missing covers or scene-only previews cannot be approved. Existing final packages are not overwritten. Return to review retains final copies. A spoken/typed approval in this chat can use the same /api/approve endpoint; do not approve based on rendering alone. Tests exercise delivery in an isolated temporary folder, not the user's Desktop.

## Plan approval workflow

Source intakes have title names, `stage: source`, and no finished cover. Their sibling `edit-plan.json` holds hooks, strategy, stock defaults, source asset needs and the complete proposed script table. Edit plan fields or edit/overlay cells, then Save Plan Changes. Approve Edit Plan creates a revision-bound job in `notes.json` → `edit_queue`; it does not ship the source or approve a final. Saving modifications invalidates plan approval and removes the old queued job. Source text/timestamps remain immutable in the plan UI.

The Editing Room approved edits thread heartbeat checks jobs every five minutes. It verifies plan revision and source fingerprint before acting, records progress, and requests required assets rather than substituting invented evidence. A finished draft requires its separate Approve & Save Final action. Workflow UI, local server and heartbeat run on this Mac; keep Codex available for background agent work.

## Simplified room — October 9 workflow update

The strategy is read-only prose, with title/verbal hook, opening visual and overlay approach. Detailed composition, cuts and cover direction are collapsed. The three-column script remains visible and clickable. Request revisions in the corresponding Codex chat; there are no settings inputs or embedded chatbot. The plan-approval buttons have been removed. Final delivery still requires Approve & Save Final with the finished video and deliberate cover.

Use `/?project=PROJECT_ID` in each video chat to lock the room to that video; refresh each open tab once for the new UI. The five-minute automation is paused. Loading or refreshing the room does not launch an agent. Initial trim/audio exports are explicitly labeled First Trim, with visual treatment pending; these are not finished deliveries.

Remove from review hides the entire selected video project, including later versions, without deleting any media, plans, covers or feedback. `/api/remove` accepts `{group: PROJECT_ID, removed: false}` to restore it. Removal is separate from final approval.

## Waveform trim timeline

The timeline displays the exact selected version’s audio, with zoom up to 32×, playback cursor and draggable selection. Click to seek; drag or enter start/end seconds to select, then Cut selection. Red ranges mark deletions; Undo cut removes a range. Play selection includes 0.3 seconds of context. Preview cuts skips marked ranges in browser playback; this is an approximate preview, not the encoded join. Save trims stores a validated, fingerprint-bound cut list under notes.json → trim_requests. It does not render or approve delivery. Ask the video's Codex chat to apply saved trims; the agent must review speech edges/joins and update picture, audio, script mappings and visual timing together. No automatic five-minute polling is resumed. Waveforms are cached locally in .cache/review-waveforms.

## Compact workspace and instant trim playback

The header, video, compact hook/strategy strip, internally scrolling script, and thin bottom timeline fit the viewport without page scrolling. Instruction/provenance paragraphs are hidden from the main UI. Select silence marks quiet peak-amplitude runs; Trim silence adds them to the cut list and immediately skips them in playback. Default minimum is 40 ms at −40 dB; both controls are adjustable. Internal quiet ranges preserve 10 ms at each edge. Undo all restores all ranges. Browser seeking is an approximate playback edit, not an encoded join; a saved MP4 still requires export and boundary review. Every source/video remains unchanged by these UI controls.
