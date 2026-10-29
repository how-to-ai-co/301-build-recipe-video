> ## Where account identity actually lives
>
> **This document contains no account numbers, no logins and no keys, on
> purpose.** Every credential and every account identifier belongs in your
> team's shared password manager. Ask whoever runs it for access to the
> Replicate, ElevenLabs, Kling and (if you run ads) Meta entries.
>
> That is not squeamishness. IDs pasted into a document go stale the moment an
> account changes, they travel further than the document does, and they give a
> convincing opening to anyone phoning up pretending to be support. The vault
> stays correct and the document stays shareable.
>
> **The one thing you genuinely need is a check, not a number.** If you have
> more than one login with any of these services — a personal one and a company
> one is the usual pair — only one of them is funded, and the two look identical
> in the UI. Before you generate anything, read the credit balance on the
> account you are about to spend from: **a balance in the range you funded means
> you are on the right account; a small leftover or trial balance means you are
> not.** Stop and switch rather than topping up the wrong one. That test keeps
> working after every ID in any document has changed.

> **Paths in this section refer to the `engine/` folder in this bundle.**
> Scripts live in `engine/scripts/`, the key file lives at `engine/.env`, and
> Remotion sources live in `engine/src/`.
>
> **On the dynamic words import.** An audit pass once flagged
> `require(`../public/words/${...}`)` in the generated `Root.tsx` as unrunnable.
> It is not, in this bundle: Remotion bundles with webpack, which resolves a
> template-literal require into a context module over the whole directory. It
> was tested with two ads and rendered four files. Trust the test, not the
> claim, and if you ever switch bundlers, re-test it first.

> **Extra note for this section:** it contains NO key values, only variable
> names and placeholders. Keep it that way.

# 5. Accounts, API keys, and environment setup

This section assumes you have never touched this pipeline. Work through it top
to bottom. At the end you will have: a machine that can run the pipeline, an
`engine/.env` holding two keys that have never appeared in a terminal or a chat
log, a Kling subscription reachable both in the browser and from Claude Code,
and a verified balance on every paid service.

---

## 5.0 SECURITY — read this before you create a single key

**Six rules. Rule 1 is not optional and comes before you create any key.**

**1. Make `.env` ignorable everywhere, first.**
`engine/.gitignore` line 1 (`.env`) protects the key file **inside `engine/`
only**. If you drop the `engine/` folder into a larger repo, that repo's root
`.gitignore` probably has no `.env` rule at all, and a `.env` created at the
repo root — or anywhere except `engine/` — is committable. Verify, then fix,
before you make a key:

```bash
cd /path/to/your/repo
git check-ignore -v engine/.env        # must print a match
git check-ignore -v .env               # if this prints nothing, it is NOT ignored

# if anything above is unprotected:
printf '\n# secrets — never commit\n.env\n*.env\n.env.*\n' >> .gitignore
git check-ignore -v .env engine/.env   # both must now print a match
```

Also check history once on any repo you inherit: `git ls-files | grep -i env`
and `git log --all -- engine/.env` should both be empty. If they are, you are
preventing a leak, not cleaning one up — the cheap side of that line.

**The trap that makes rule 1 urgent.** Any doc, tutorial or teammate that tells
you to *"create `.env` in the project root"* is pointing you at the one place
the `engine/` ignore rule does not cover. The pipeline reads `engine/.env`,
nothing else. Put the file there and only there.

**2. Never let a key value reach a terminal, a log, or a chat.**
No `cat engine/.env`. No `echo $REPLICATE_API_TOKEN`. Never pass a key as a
command-line argument — arguments are visible to any other process via `ps` and
land in shell history. Every write to `.env` uses the `read -s` pattern in
§5.3. The loaders in this bundle honour this: `scripts/generate.py` reads the
key and never prints it — *"Key stays in .env, never printed"* — and the
consolidated loader in §5.10 keeps the same contract. Preserve that property in
anything you add.

**3. Only spend on keys you created yourself.** A key you were handed in a
chat, an email, a ticket or a doc has already travelled and must be treated as
public. Create fresh keys in each provider's dashboard, verify them with the
free calls in §5.11, and rotate anything of unknown history using the
procedure in §5.4.6 — create and verify the replacement first, delete the old
one last, so you are never locked out mid-render.

**4. `~/.claude.json` is a secret file too.** It holds the MCP server registry,
and other servers registered in it may store plaintext API keys in their `env`
blocks. Never paste that file into a chat, a ticket, or a screen share, and
never `cat` it. Edit it with the script in §5.7, which touches only the one
entry it needs to.

**5. If a key was ever visible, it is burned.** Screen share, screenshot,
pasted error message, pasted `.env`, a support ticket, a commit that got
reverted. There is no partial exposure. Create a new key, verify the new one
works, then delete the old one — in that order, so you are never locked out
mid-render.

**6. Nothing is backed up unless you back it up.** Keys are cheap to re-issue;
generated video is not — a folder of finished renders represents real API
spend. Get finished mp4s to cloud storage the day they render, and push the
repo to a remote before the machine holding it has a bad day.

---

## 5.1 What the pipeline actually needs

| Service | What it does here | Auth lives in | Paid? |
|---|---|---|---|
| **fal** (the default, §5.14) | Voiceovers (MiniMax, ElevenLabs voices, Chatterbox clones), Seedance 2.5 talking takes, lip sync, video background removal, Kling silent clips, Nano Banana Pro stills, via `scripts/fal.py`. Full detail in parts/55 | `engine/.env` → `FAL_KEY` | Yes, prepaid balance, metered per job. The account **locks** when the balance runs out |
| **Replicate** | Video and image generation (Seedance 2.0, Veo 3.1, Kling 2.5, nano-banana-pro) via `scripts/generate.py` | `engine/.env` → `REPLICATE_API_TOKEN` | Yes, metered per prediction, card on file. Check whether auto-reload is on before your first batch |
| **ElevenLabs** | Voiceover, and the Music API if you use it. **The free tier blocks professional voice clones AND the Music API** — see §5.5.2 | `engine/.env` → `ELEVENLABS_API_KEY` | Free tier exists (10,000 credits). Creator (~$22/mo) is needed to unlock cloned voices *and* the Music API |
| **Kling** (web) | Kling 3.0 / Omni multi-shot with native audio — the dialogue format in parts/60 | Browser login, your funded Kling account | Yes, subscription (Premier at time of writing), credit-metered |
| **Kling** (MCP) | Same account, driven from Claude Code instead of the browser | `~/.claude.json` → `mcpServers.kling`, **OAuth, no key stored** | Spends the same membership credits |
| **Meta** (optional) | Pixel + ad account, only if you run the finished ads yourself | `~/.claude.json` → `mcpServers.meta-ads`, OAuth | Ad spend, separate from all of the above |

Up to three secrets go in `engine/.env`, and only the ones you actually use.
Most setups need just the first:

```
FAL_KEY
ELEVENLABS_API_KEY
REPLICATE_API_TOKEN
```

`scripts/fal.py` matches `FAL_KEY=` literally. Spell the Replicate one
exactly too: `REPLICATE_API_TOKEN`, *TOKEN* not *KEY*.
`scripts/generate.py` matches the line prefix literally, so a line named
`REPLICATE_API_KEY=` would be silently invisible to it and you would get
"not set in .env" while staring at a key that is right there.

---

## 5.2 Machine prerequisites

Versions below are what the pipeline was built and tested against. Newer
patch releases are normally fine; do not go older.

```bash
# Homebrew binaries
brew install ffmpeg          # ffmpeg + ffprobe, used by grading and QC
```

| Tool | Tested version |
|---|---|
| python3 | 3.11 |
| node | v22 (Remotion needs Node; `engine/package.json` pins Remotion ^4.0.500) |
| ffmpeg / ffprobe | any current Homebrew build |

Python packages, from `engine/requirements.txt`:

```bash
python3 -m pip install -r engine/requirements.txt
# openai-whisper  librosa  numpy  scipy  pillow
```

What each one is for, so you know what you can skip. Mapping taken from the
actual `import` lines, file by file:
- `numpy` / `scipy` — music synthesis. Imported by `scripts/bed.py` only, which
  writes the original bed `public/audio/bed_phrygian.wav`.
- `librosa` — imported by `scripts/prosody.py` only. It is the uptalk / pacing
  gate on voiceover takes, not part of anything visual.
- `pillow` (`PIL`) — caption and card rendering, imported by
  `scripts/render_aerial.py`.
- `openai-whisper` — `scripts/timings.py` uses `whisper.load_model("small")`
  for the word-level caption timings. First run downloads the model; after
  that it is local and free.
- `scripts/grade.py` imports **no** third-party audio or image library — it
  shells out to ffmpeg.

**Voiceover has no local dependency in this bundle.** Your first voiceover
comes from ElevenLabs (§5.5) or from your own recording; either way,
`scripts/timings.py` turns the finished wav into the word-timing JSON the
formats consume. No TTS model runs on your machine.

Node side:

```bash
cd engine && npm install     # Remotion 4.0.500 + React 19
```

---

## 5.3 Create `engine/.env` safely

The file lives at `engine/.env`, at the engine root next to `package.json`.
Create it at mode `600` and keep it that way.

**The `read -s` pattern.** `read -s` does not echo what you type, and the value
never becomes part of a command line, so it never reaches shell history, the
process table, or a chat transcript. Copy the key to your clipboard from the
provider UI, run the command, paste, press Enter.

```bash
cd /path/to/engine
umask 077                       # anything created below is 600 from birth
touch .env && chmod 600 .env

read -r -s -p 'FAL_KEY: ' V \
  && printf '%s=%s\n' FAL_KEY "$V" >> .env \
  && unset V

read -r -s -p 'REPLICATE_API_TOKEN: ' V \
  && printf '%s=%s\n' REPLICATE_API_TOKEN "$V" >> .env \
  && unset V

read -r -s -p 'ELEVENLABS_API_KEY: ' V \
  && printf '%s=%s\n' ELEVENLABS_API_KEY "$V" >> .env \
  && unset V

chmod 600 .env
cut -d= -f1 .env                # prints ONLY the names. Safe. Never `cat .env`.
```

Notes on why it is written exactly that way (tested):
- `-r` stops backslashes in a key from being eaten
- `"$V"` is quoted, so a `$` inside a key is not expanded (tested with a value
  containing a literal `$` — round-tripped intact)
- `unset V` clears the variable so it cannot leak from a later `env` dump
- `cut -d= -f1` is the only inspection command you should ever run on `.env`

Skip any `read` block for a service you are not using. With all three, the
finished file looks like this, with the real values where the placeholders
are:

```
FAL_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 5.4 Replicate

Replicate is the general-purpose model host. `scripts/generate.py` wraps it:
create a prediction, poll, download the output — with a price printed and a
dry run by default (see parts/50).

### 5.4.1 Sign up
1. Go to `https://replicate.com` and click **Sign in**. Replicate authenticates
   through GitHub, so you need a GitHub account first.
2. Use one account per team, and record it in the vault. Spend history and the
   card live on the account, so a personal signup that "was just for testing"
   becomes the account of record by accident. Decide up front.

### 5.4.2 Plan and money
There is no subscription. Replicate is pure metered pay-as-you-go against a
prepaid balance, billed per prediction (roughly, per second of GPU time on the
model you called).

- **Check the auto-reload setting before your first batch.** With auto-reload
  on there is no natural stop: video models burn a balance fast, and a single
  working session of video generation can run into the low hundreds of
  dollars. Read §5.12 before you run anything.

### 5.4.3 Find the token in the UI
1. Signed in, open **`https://replicate.com/account/api-tokens`** (also
   reachable from the avatar menu, top right → **API tokens**).
2. Click **Create token**, name it something traceable — include the project
   and the provider in the name, e.g. `yourproject-replicate-video`. A name
   that could belong to any provider's key will eventually make someone delete
   the wrong one during a rotation.
3. The token is shown **once**. It starts with `r8_`. Copy it now.

### 5.4.4 Put it in `.env`
Env var name: **`REPLICATE_API_TOKEN`**. Use the `read -s` pattern from §5.3.

### 5.4.5 Verify with the cheapest possible call
The cheapest call is a **free** one: an account metadata read that creates no
prediction. `GET https://api.replicate.com/v1/account` returns who the token
belongs to. See the script in §5.11, which does both services at once.

Do **not** verify by running a model. A "quick test render" on a video model
is a real charge.

### 5.4.6 Rotation procedure — use it whenever a key may have been seen
Order matters: create and verify the replacement first, delete the old one
last, so you are never locked out mid-render.

```bash
cd /path/to/engine

# 1. In the browser: replicate.com/account/api-tokens -> Create token.
#    Name it with a -2 suffix so old and new are unambiguous. Copy it.

# 2. Replace the line in .env without ever echoing either value.
read -r -s -p 'new REPLICATE_API_TOKEN: ' V
umask 077
grep -v '^REPLICATE_API_TOKEN=' .env > .env.new || true
printf '%s=%s\n' REPLICATE_API_TOKEN "$V" >> .env.new
mv .env.new .env
chmod 600 .env
unset V

# 3. Verify the NEW token works (free call, see 5.11)
python3 scripts/check_keys.py

# 4. Only once step 3 passes: in the browser, ON THE RIGHT PROVIDER's
#    dashboard, delete the OLD token. If your key names do not say which
#    provider they belong to, confirm before deleting anything.
```

Tested against a dummy `.env`: the replace preserves the other key, drops only
the old `REPLICATE_API_TOKEN` line, and leaves the file at mode 600.

The same shape works for `ELEVENLABS_API_KEY` — swap the variable name.

---

## 5.5 ElevenLabs

Used for voiceover, and for the Music API if your plan includes it.

### 5.5.1 Sign up
1. `https://elevenlabs.io` → **Sign up**. Free tier gives you an account and a
   key immediately.

### 5.5.2 Plan and money — the free-tier trap
**The free tier (10,000 credits) blocks TWO things, not one:**

1. **Professional / cloned voices** — calling one on the free tier returns
   **403 `subscription_required`** (*"Professional voices require a Creator
   tier subscription"*). If you clone your own or a founder's voice, that
   clone is unusable until the account is upgraded.
2. **The Music API** (`https://api.elevenlabs.io/v1/music`) — *"not available
   for free users"*. Do not plan a music pass around it until the account is
   upgraded. This bundle does not depend on it: beds composed by
   `scripts/bed.py` are original and rights-clean (§5.8).

- **Creator tier, roughly $22/mo, unlocks cloned voices and the Music API.**
  That is the purchase decision in front of you if you want either.
- Stock voices are a reasonable free-tier starting point, but whether a given
  stock voice works on free is not something to assume — run one short call
  and check, after `check_keys.py` has told you your tier.
- Voice IDs come from the ElevenLabs voice library UI (each voice's page shows
  its ID). Keep your chosen IDs in your own config, not scattered through
  scripts — they are not secrets, but they are per-account.

### 5.5.3 Find the key in the UI
1. Signed in, open **`https://elevenlabs.io/app/settings/api-keys`** (also
   reachable from the profile menu → **Settings** → **API Keys**).
2. **Create API Key**, name it, copy it. It starts with `sk_`. Shown once.
3. **Scope it to what the pipeline uses:** Text-to-Speech, Music Generation
   and Voices-read only. A key with broader scope buys nothing this pipeline
   uses and costs you more if it leaks.

### 5.5.4 Put it in `.env`
Env var name: **`ELEVENLABS_API_KEY`**. `read -s` pattern, §5.3.

### 5.5.5 Verify with the cheapest possible call
`GET https://api.elevenlabs.io/v1/user/subscription` is free and returns the
plan tier plus the character quota. It also answers the question you actually
care about — *am I on free, and will cloned voices 403?* — without spending a
single character of quota. Covered by §5.11.

---

## 5.6 Kling — the web subscription

Kling 3.0 is where the dialogue format lives (parts/60), because it is the
only route with multi-shot + native audio + reference images together.

### 5.6.1 The multiple-login trap. Read this before you click anything.
If your team has ever signed up twice — a personal trial and a funded company
account is the classic pair — the two look **identical** in the UI, and only
one of them carries the subscription.

The single fastest way to know you are on the wrong account: *the credit
balance is a small trial number instead of the thousands your plan grants.*
A wrong balance is not a stale display; it is a different login. Stop and
switch. Never top up the account you happen to be logged into to make an
error go away.

Browser complications, if you drive Kling through a Claude browser extension:
- If more than one Chrome profile is paired with the extension, confirm which
  profile holds the funded login **before** connecting, and have the account
  owner click Connect in that window. Extensions happily pair with whichever
  profile answered first.
- **Create the tab inside the MCP tab group and front it — tabs outside the
  group can render 0x0.** A 0x0 tab looks like a blank, broken Kling app, not
  like a tab problem.

URL rule, learned the hard way: use **`kling.ai/app/...`** URLs, never
`app.klingai.com/global/...` — the latter redirects and drops the session.

### 5.6.2 Sign up and subscribe
1. Go to `https://kling.ai` and sign in with the account your team funds.
2. Subscription lives under the membership / upgrade page. The plan this
   pipeline was run on is **Premier** (credit-metered; pick the tier whose
   monthly credit grant covers your planned volume, see §5.6.3 for the
   arithmetic).
3. Confirm the balance on the **Credit Details** page. It breaks the number
   into Membership / top-up / bonus, which is how you catch the wrong-login
   case.

### 5.6.3 Credits expire. Put it in the calendar.
The membership grant carries a fixed grant timestamp and a fixed expiry
timestamp, both shown on the Credit Details page. **Use those two timestamps,
do not do the arithmetic yourself** — a "monthly" grant runs calendar month to
calendar month, which is 30 or 31 days depending on when it was issued.
Unspent credits are lost; they do not roll over.

Sizing rule of thumb: at the measured rate of **180 credits for one 15s 1080p
Omni take** (§5.12), an 8000-credit monthly grant is about **44 takes of that
size** for the month. Budget your re-rolls against that number, not against
the raw credit figure.

---

## 5.7 Kling — MCP registration in `~/.claude.json`

This is how Claude Code drives Kling directly instead of clicking through the
browser. Use the MCP; it is the working route.

### 5.7.1 The one detail that wastes a whole session if you miss it

> **MCP tools load ONLY in a session started AFTER the config entry was added.**

Adding the entry to a running session does nothing. The tools will not appear,
and you will conclude the config is wrong when it is fine. A previous session
was stuck on exactly this. **Add the entry, quit Claude Code entirely, start a
new session, then look for the tools.**

### 5.7.2 The entry — no secret in it
The registration carries **no API key**. Kling MCP is an HTTP server that
authorizes over OAuth inside the app. This is the exact entry:

```json
{
  "mcpServers": {
    "kling": {
      "type": "http",
      "url": "https://kling.ai/mcp"
    }
  }
}
```

### 5.7.3 Add it without hand-editing the file
`~/.claude.json` is large and holds unrelated config, possibly including
plaintext keys for other servers. Do not open it in an editor and do not paste
it anywhere. Save this as `add_kling_mcp.py` and run it. It backs up first, is
idempotent, and touches only the one entry.

**Quit Claude Code before you run it.** Claude Code owns this file and writes
it on exit. Edit it underneath a running session and the session can overwrite
your change, which reads as "the script didn't work." You have to restart
anyway (§5.7.1), so quit first, run the script, then start the new session.
Also note the script re-serialises the whole file with `indent=2`, so the
formatting of unrelated config will change even though no value does. That is
cosmetic, and the `.bak` next to it is your undo.

```python
#!/usr/bin/env python3
"""Add the Kling MCP server to ~/.claude.json, idempotently, with a backup.

~/.claude.json is a large file that also holds unrelated config. Do not
hand-edit it. This script backs it up, adds only the "kling" entry, and leaves
everything else in place.

The entry carries NO secret. Kling MCP is an HTTP server that authorizes over
OAuth in the app, so there is no API key to store here.

Usage:  python3 add_kling_mcp.py [--path ~/.claude.json]
"""
import argparse
import json
import pathlib
import shutil
import sys

ENTRY = {"type": "http", "url": "https://kling.ai/mcp"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=str(pathlib.Path.home() / ".claude.json"))
    args = ap.parse_args()

    p = pathlib.Path(args.path).expanduser()
    if not p.exists():
        sys.exit(f"{p} not found. Start Claude Code once so it is created.")

    cfg = json.loads(p.read_text())
    servers = cfg.setdefault("mcpServers", {})

    if servers.get("kling") == ENTRY:
        print("kling already registered, nothing to do")
        return

    backup = p.with_suffix(".json.bak")
    shutil.copy2(p, backup)
    servers["kling"] = ENTRY
    p.write_text(json.dumps(cfg, indent=2) + "\n")
    print(f"backup written to {backup}")
    print("kling registered. START A NEW CLAUDE CODE SESSION - MCP tools only "
          "load in a session started AFTER the config entry was added.")


if __name__ == "__main__":
    main()
```

Tested: run twice against a dummy config it adds the entry then reports
"already registered", leaves unrelated config intact, and writes the `.bak`.

The CLI equivalent is `claude mcp add --transport http kling https://kling.ai/mcp`.
The JSON route above is the one that is verified.

### 5.7.4 Authorize, then verify
1. Run the script. **Quit Claude Code. Start a new session.**
2. Confirm the tools exist: `ToolSearch "+kling"`. You should see
   `mcp__kling__who_am_i`, `query_membership_and_credits`, `file_upload`,
   `text_to_image`, `image_to_image`, `text_to_video`, `image_to_video`,
   `query_tasks`.
3. Authorize with `/mcp` in an **interactive** session — it opens an OAuth
   browser flow. **The browser must be logged into the funded account.** If it
   is logged into a personal or trial login you will bind the MCP to an
   unfunded account, and every generation will fail or spend the wrong wallet.
4. **Cheapest possible verification — both calls are free, neither generates
   anything:**
   - `mcp__kling__who_am_i` → expect the user ID recorded in your vault for
     the funded account
   - `mcp__kling__query_membership_and_credits` → expect your plan name and a
     membership balance in the range your subscription grants

   **If the balance is a small trial number, you are on the wrong login. Stop.**

### 5.7.5 Billing, resolved: there is no second meter
Measured on a live account: `query_membership_and_credits` read the membership
balance before a job and exactly the job's cost less after it (8000 → 7820
across a 180-credit job). The MCP spends the **membership credits**, not a
separate API balance. There is nothing else to fund.

Cosmetic gotcha: the MCP appears to exclude bonus credits, so the MCP balance
and the web Credit Details page can disagree by the bonus amount. Not a bug,
do not chase it.

### 5.7.6 Uploading reference images through the MCP is free
Two steps. Call `mcp__kling__file_upload` with filename / contentType / size to
get a single-use `ticket` and `uploadUrl`, then POST the bytes yourself:

```bash
curl -X POST https://kling.ai/api/mcp/files \
  -F "ticket=$TICKET" \
  -F "file=@path/to/image.jpg;type=image/jpeg"
```

The response `data.url` is the reference URL you pass to a generation.
**Tickets expire in about 10 minutes**, so upload immediately before the
generation that uses them, not the night before. Image spec: JPG, under 4K,
≤30MB, aspect ratio within 1:2.

---

## 5.8 Music — licensing is a gate, not a footnote

**Rule: no track goes into an ad without documented provenance.** "Someone
sent me the file" is not provenance. If a track was generated on a music
service, the *plan* it was generated on determines the commercial rights, so
record the account and plan alongside the file. If you cannot establish where
a track came from, do not put it under paid media — a licensing question found
after launch reaches every cut that used the track, and a bed reused across a
wave can turn one undocumented file into twenty exposed ads.

The clean path ships in this bundle and has no rights problem at all:

- `public/audio/bed_phrygian.wav` — **originally composed music generated in
  code by `scripts/bed.py`**. `bed.py` writes exactly that one file, and you
  can regenerate or modify it from source. Zero rights encumbrance, zero
  subscription.

Prefer these, or beds you generate yourself with `bed.py`, until you have a
music source with rights you can show on paper. Keep `public/audio/` clean:
anything that appears in that folder will eventually be assigned to an ad by
someone who assumes everything in it is cleared.

---

## 5.9 Meta — pixel and ad account (no key in `.env`)

Included because an operator who runs the finished ads will look for it. Meta
is not part of the generation pipeline and has no entry in `engine/.env`.

- Your ad account and pixel IDs live in your Business Manager; record them in
  the vault, not here.
- **Confirm who owns the ad account and the pixel before you spend or before
  any agency transition.** Ownership that everyone "believes" but nobody has
  verified in Business Manager settings is the classic way a pixel's history
  walks out the door with a contractor. Check the actual owner in Business
  settings; treat anything else as unverified.
- Claude Code reaches Meta through an OAuth MCP server, no key stored:
  `~/.claude.json` → `mcpServers["meta-ads"] = {"type": "http", "url": "https://mcp.facebook.com/ads"}`
- Authorize the same way as Kling: `/mcp` in an interactive session. The
  restart rule in §5.7.1 applies to this entry too.

---

## 5.10 Hardened key loader — `scripts/envkey.py`

`scripts/generate.py` carries its own minimal loader for
`REPLICATE_API_TOKEN`. For anything else you write against `.env`, do not
hand-roll another parser — three near-identical hand-rolled loaders in the
original pipeline disagreed on duplicate handling, error messages and path
resolution, and one of them crashed with a raw `StopIteration` when the key
was missing. This module is the consolidation. Save it as
`engine/scripts/envkey.py`.

What it handles, deliberately:

| Behaviour | `envkey.py` |
|---|---|
| How `.env` is located | resolved against **this file's** location (`engine/.env`), never the shell's cwd — a loader that resolves against cwd breaks the first time a script is invoked from another directory |
| Duplicate name in file | **first** wins |
| Key missing | clean `sys.exit` naming the variable, the full path, and the `read -s` command to fix it |
| `.env` file missing | clean `sys.exit` with create instructions |
| Comments, blank lines, `export ` prefix, quoted values | handled — a bare line-prefix match treats `export FOO=` or an indented line as invisible, which reads as "key not found" while the key is right there |
| Prints the key | **never** |

Two edge cases to know about, both deliberate:

- **Empty value.** A line reading `REPLICATE_API_TOKEN=` with nothing after it
  is treated as missing and exits. A loader that returns the empty string
  instead sends `Authorization: Bearer ` and you debug a 401 from the API
  rather than a problem in your file. Fail early.
- **Quote stripping.** `_parse` strips one matched pair of surrounding quotes.
  If a provider ever issues a key whose real first and last characters are
  both `"` or both `'`, this returns a different string than a naive parser
  would. No real key looks like that — Replicate keys start `r8_`, ElevenLabs
  keys start `sk_` — but know the behaviour exists.

There is deliberately **no** `os.environ` fallback. A stale exported variable
silently shadowing `.env` is exactly the kind of thing that costs a debugging
session on a paid API.

### `scripts/envkey.py` — complete file

```python
#!/usr/bin/env python3
"""Single loader for the API keys held in engine/.env.

The contract:

  - the key lives in engine/.env, one directory above this scripts/ folder
  - the key is READ ONLY. Nothing in this module prints, logs, or puts a key
    value into an error message. "Key stays in .env, never printed."
  - stdlib only, no third-party dependency
"""
import pathlib
import sys

# Resolve against THIS file, not the shell's cwd. scripts/ sits one level
# below the engine root, so .env is at parent.parent — the same convention
# generate.py uses for ROOT.
ENV_PATH = pathlib.Path(__file__).resolve().parent.parent / ".env"

_HINT = (
    "  Add it without it ever reaching your shell history or a chat transcript:\n"
    "    read -r -s -p '{var}: ' V && printf '%s=%s\\n' {var} \"$V\" >> {path} && unset V\n"
    "    chmod 600 {path}"
)


def _parse(text):
    """NAME=VALUE, one per line. First occurrence of a name wins."""
    out = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name, value = name.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out.setdefault(name, value)  # first wins
    return out


def key(name):
    """Value of `name` from engine/.env, or exit with a message a human can act
    on. The message names the variable and the file. It never contains a key."""
    try:
        text = ENV_PATH.read_text()
    except FileNotFoundError:
        sys.exit(f"{ENV_PATH} does not exist. Create it, then add {name}:\n"
                 + _HINT.format(var=name, path=ENV_PATH))
    value = _parse(text).get(name)
    if not value:
        sys.exit(f"{name} is not set in {ENV_PATH}\n"
                 + _HINT.format(var=name, path=ENV_PATH))
    return value


def present(name):
    """True if `name` has a non-empty value. Safe to print the result of."""
    try:
        return bool(_parse(ENV_PATH.read_text()).get(name))
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    # Presence check only. Prints the NAME, whether it is set, and the length
    # (a short length catches a truncated paste). Never the value.
    for n in ("REPLICATE_API_TOKEN", "ELEVENLABS_API_KEY"):
        if present(n):
            print(f"{n:22} present  len={len(key(n))}")
        else:
            print(f"{n:22} MISSING")
```

Tested against a dummy `.env` containing a comment, a blank line, an
`export `-prefixed quoted value, and a duplicated name: comment and blank
skipped, `export ` stripped, quotes stripped, first duplicate wins, empty
value treated as missing, missing-var and missing-file paths both produce the
actionable message and exit 1. No value printed.

---

## 5.11 One-shot verification — `scripts/check_keys.py`

Both calls are metadata reads. **Neither creates a prediction, generates a
second of audio, or costs anything.** No key value is printed. Run it after
creating keys, after any rotation, and on any new machine. Save it as
`engine/scripts/check_keys.py`, next to `envkey.py`.

```python
#!/usr/bin/env python3
"""Verify the keys in engine/.env with the cheapest possible calls.

Both calls are free metadata reads. Neither creates a prediction nor generates
audio. Do NOT verify a key by running a model - on a video model that is a real
charge. No key value is printed by this script.

Run from the engine root:  python3 scripts/check_keys.py
"""
import json
import sys
import urllib.error
import urllib.request

from envkey import key


def get(url, headers):
    req = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def check_replicate():
    # GET /v1/account is free: it returns who the token belongs to.
    try:
        acct = get("https://api.replicate.com/v1/account",
                   {"Authorization": f"Bearer {key('REPLICATE_API_TOKEN')}"})
    except urllib.error.HTTPError as e:
        print(f"REPLICATE  FAIL {e.code} {e.reason}"
              "  (401 = bad, revoked, or rotated token)")
        return False
    print(f"REPLICATE  ok    account={acct.get('username')} "
          f"type={acct.get('type')}")
    return True


def check_elevenlabs():
    # GET /v1/user/subscription is free: it returns the plan tier and the
    # character quota. Tier is the thing that matters here - on 'free',
    # professional/cloned voices return 403 subscription_required and the
    # Music API is refused.
    try:
        sub = get("https://api.elevenlabs.io/v1/user/subscription",
                  {"xi-api-key": key("ELEVENLABS_API_KEY")})
    except urllib.error.HTTPError as e:
        print(f"ELEVENLABS FAIL {e.code} {e.reason}  (401 = bad key)")
        return False
    print(f"ELEVENLABS ok    tier={sub.get('tier')} "
          f"chars={sub.get('character_count')}/{sub.get('character_limit')}")
    if sub.get("tier") == "free":
        print("           NOTE free tier: cloned/professional voices will 403 "
              "subscription_required, and the Music API is blocked.")
    return True


if __name__ == "__main__":
    ok = check_replicate()
    ok = check_elevenlabs() and ok
    sys.exit(0 if ok else 1)
```

**Honest status: this script has not been run against a real key** — doing so
requires live key values, which this document deliberately never touches. What
*was* checked: an unauthenticated `GET` to
`https://api.replicate.com/v1/account` and to
`https://api.elevenlabs.io/v1/user/subscription` each returned **401**, not
404. 401-not-404 is the whole point — it proves the path is live and that the
only thing missing is a valid key. If either ever returns 404, the endpoint
moved; check the provider's current API reference.

The response *field* names (`username`, `type`, `tier`, `character_count`,
`character_limit`) are not verified — an unauthenticated 401 returns no body to
read them from. If a field prints as `None`, the call still succeeded; only the
key name in the f-string is wrong.

Kling has no equivalent script because it has no key. Verify it with the two
free MCP calls in §5.7.4.

---

## 5.12 COST CONTROL

### What each service charges

**Kling — 12 credits per second of output, every v3_0 tier.** Measured.

| Output | Credits |
|---|---|
| 15s (the max) | 180 |
| 9s | 108 |
| 8s | 96 |

Duration was the only lever that moved the price in testing. **There is no
discount for one long generation**, so splitting a batch into shorter
generations costs the same and produces better output. Splitting saves money by
reducing re-rolls.

**Kling image models — the spread is 17x.** Measured. The comparison is three
models on one fixed workload; keep that workload in mind or the numbers are
not comparable.

| Model | Credits for **2 images @ 2k** | Use it for |
|---|---|---|
| `gpt-image-2` | **70** | Best analog / film-grade fidelity, best precision instruction following. Reserve it for the shots that need exactly that |
| `gemini-3.1-flash-image` (Nano Banana 2) | **30** | **Rejects likeness work.** Identity-matching prompts fail in ~5s with no error text |
| `kling-image-v3_0_omni` | **4** | Holds face identity from a reference. **The default for everything else** |

70 ÷ 4 = the 17x. Route by default to the 4-credit model; reaching for
`gpt-image-2` out of habit is a 17x overspend.

**`kling-image-o1` is a fourth model but is NOT on that table**, and it was
never priced on the 2-images-at-2k workload. What is recorded is a different
measurement: **2 credits for one surgical single edit** (removing debris from
a shot — *"2 credits, surgical, worked first try"*). Use it for exactly that,
and do not treat "2" as a like-for-like comparison against the 70 / 30 / 4
column.

**fal**: metered per job against a prepaid balance. When the balance runs
out the account locks and every call returns 403 until someone tops it up
(§5.14.2). `scripts/fal.py` does not print prices, so read the rate on each
model's fal.ai page and state it before `--go`. In the projects this engine
was built from, fal spend was never counted per run, so there is no measured
number to give you here. Count yours.

**Replicate** — metered pay-as-you-go against a prepaid balance. If
auto-reload is on there is no ceiling except the one you impose; a single
working session on video models can run into the low hundreds of dollars.

**ElevenLabs** — free tier is 10,000 credits. Creator ~$22/mo is the upgrade
that unlocks cloned voices **and the Music API**, which is also blocked on
free.

**Kling subscription** — a monthly plan that grants credits which **expire on
a fixed date**. Read the grant and expiry timestamps on the Credit Details
page; do not assume a rolling 30 days (§5.6.3). Unspent credits are lost.

### The rules that keep spend sane

**1. Checkpoint one shot end-to-end before batching.** Generate one. Take it
all the way through assembly. Have a human watch and *listen* to it. Report
spend at the checkpoint. Only then batch. This rule exists because batches
built on an unverified setup have been thrown away whole.

**2. Stop-loss decided in advance.** Before the first generation, write down
the number of credits or dollars at which you stop and go back to the plan.
Deciding mid-run, with sunk cost already on the table, does not work.

**3. `enable_audio` defaults to FALSE on Kling Omni. Set it to `true`.**
Silent takes are the single easiest way to waste credits here. A silent 15s
take is 180 credits of nothing.

**4. `resolution` defaults to `4k`. Set `1080p`.** 1080p is the finishing
resolution for these ads and it costs less.

**5. Never resubmit because a job "looks stuck."** `query_tasks` **is badly
stale** — measured three separate times: a finished image job reported
`QUEUING` for ~8 minutes after completing in 106s; a 58-second job reported
`RUNNING` for ~14 minutes; `finishTime` is set early and is meaningless while
status is not `COMPLETED`. The credits endpoint appears cached too — the
balance did not move across a 70-credit charge. **Poll on 5-minute-plus
intervals, expect lag, and do not swap models or resubmit on a phantom hang.**
A model swap was nearly wasted on exactly this.

**6. Cap a generation at about 3 shots.** Five shots in 15s garbles dialogue —
both 15s/5-shot takes came back with soft lip sync, and one pronounced
"designer" as "designder". Kling also ignores the shot plan under load: one take
gave shot 4 five seconds and starved shot 5 to 0.9s; another never cut to shot 5
at all. Split the batch, keeping the same `first_image` across the halves so
face and voice stay matched.

**7. Do not feed a multi-panel location sheet to Omni as a reference.** It
rendered the location sheet *as a shot*: a top-down drone view of a woman
lifting a chair over her head. For single-character dialogue use non-Omni
`kling-video-v3_0` with the scene still as `first_image` — it also renders in
half the time (6 min vs 13).

**8. From-behind shots must NOT get a face sheet.** 18 credits burned learning
this. Passing a mostly-face character sheet while demanding a shot where the
face is invisible makes the model resolve the contradiction by rendering the
face somewhere anyway — a duplicate second person, or a literal shadow-figure
on the wall. Three Kling rolls all failed identically. **The fix that worked
first try, and you need both halves of it: drop the character sheet entirely
for from-behind framings — wardrobe description carries identity — and use GPT
Image 2 for precision instruction following.** Rule: face sheet only when the
face is visible in the shot.

**8b. The inverse rule.** When the face *is* visible, the method that finally
worked is **EDIT the reference's actual frame, never recreate it**. Recreation
re-imagines the pose and re-rolls the physics every time — six drifting
attempts. The winning chain was a `gpt-image-2` EDIT of the reference frame
(pose kept pixel-level, face/wardrobe/room swapped), then a `kling-image-o1`
surgical background fix at 2 credits. Face visible means the face sheet is
allowed in the edit call.

**9. Download Kling results immediately. Result URLs expire 24 hours after the
job finishes.** Losing them means paying to regenerate.

**10. Failed jobs appear to be refunded** — the balance did not move on a
policy-rejected generation. Do not panic-spend to "make up" for a failure.

**11. Never ship audio no human has heard.** Every unheard version failed. This
is a cost rule as much as a quality rule: unheard audio is what caused whole
batches to be rebuilt.

---

## 5.13 VERIFY ON YOUR OWN ACCOUNTS

Things this document cannot know about your setup. Do not fill these in by
guessing — each has a cheap check.

1. **Which card pays each subscription, and whether auto-reload is on.** Check
   the billing page of Replicate and Kling before the first batch, and record
   the answer in the vault. Auto-reload with no stop-loss is the most
   expensive default in this pipeline.

2. **Your ElevenLabs tier.** Run `scripts/check_keys.py` — the `tier` field
   answers it in one call. Free tier gates two things, not one: cloned voices
   and the Music API.

3. **Which account the Kling MCP OAuth grant is bound to.** If more than one
   browser profile or Kling login exists on the machine, the grant may be
   bound to the wrong one. The only settling move is `mcp__kling__who_am_i`
   plus `query_membership_and_credits`, checked against the funded account in
   your vault (§5.7.4).

4. **Whether `~/.claude.json` is the right home for MCP entries on your
   machine.** That path is the user-global config on macOS. A different
   install layout, or a project-scoped `.mcp.json`, may differ. This bundle
   ships no project-level MCP config, so the user-global file is the default.

5. **Replicate per-model pricing.** `scripts/generate.py` prints the price of
   every call before spending (and is a dry run until you pass `--go`), and
   each model's Replicate page carries its current rate. Prices move; the
   printout is the truth at call time.

6. **Provenance of any music you add** beyond the shipped original beds
   (§5.8). Establish it before a track lands under paid media, not after.

7. **Your fal balance and per-model prices.** Read the balance at
   `https://fal.ai/dashboard/billing` before any long job, and the price on
   each model's fal.ai page before the first call to it.

---

## 5.14 fal

fal is the default generation account for this engine: one key covers
voiceovers, talking takes, lip sync, video background removal, silent clips
and stills. `scripts/fal.py` wraps it, with a dry run by default and the key
read only from `engine/.env` (parts/55 has every proven endpoint).

### 5.14.1 Sign up
1. Go to `https://fal.ai` and sign up. As with every provider here, use one
   account per team and record it in the vault. The card and the spend history
   live on the account.

### 5.14.2 Plan and money
There is no subscription. fal bills each job against a prepaid balance.

- **An empty balance locks the account.** Every call then returns
  `403 {"detail":"User is locked. Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing."}`.
  That error means top up, not a bad key. Do not rotate a key over it. It has
  hit mid-session on real projects, so read the balance at
  `https://fal.ai/dashboard/billing` before a long job.
- Set your own stop-loss before the first batch (§5.12). Nothing on the fal
  side stops a loop that keeps submitting jobs.

### 5.14.3 Find the key in the UI
1. Signed in, open **`https://fal.ai/dashboard/keys`**.
2. Create a key and name it with the project and the provider, e.g.
   `yourproject-fal-video`, for the same reason as §5.4.3.
3. Copy it when it is shown. A fal key is two parts joined by a colon
   (`id:secret`). Paste the whole thing, colon included.

### 5.14.4 Put it in `.env`
Env var name: **`FAL_KEY`**. Use the `read -s` pattern from §5.3.
`scripts/fal.py` reads only `engine/.env`, never the shell, so a `FAL_KEY`
exported in your terminal for another project is ignored on purpose.

### 5.14.5 Verify with the cheapest possible call
No free metadata call for fal has been verified for this engine, so
`check_keys.py` does not cover it. The cheapest proven check is one short
voice line. It is a real charge, so read the rate on the model's fal.ai page
and tell the operator before running it:

```bash
cd engine
python3 scripts/fal.py fal-ai/minimax/speech-2.8-hd \
  '{"text":"Testing.","voice_setting":{"voice_id":"English_CaptivatingStoryteller","speed":1.0},"output_format":"url"}' \
  /tmp/fal_check.mp3 --go
```

A file path printed at the end means the key works and the balance is not
empty. `fal 401` means a bad key; `fal 403` with "User is locked" means the
balance, per §5.14.2.

### 5.14.6 Rotation
The §5.4.6 procedure with the variable name swapped to `FAL_KEY`: create and
verify the new key first, then delete the old one on fal's key page.
