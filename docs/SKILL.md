---
name: just-move-the-button
description: How to extend the "Just Move the Button" interactive comic — add pages, heroes, instruments, or change the look — without breaking the design system. Read before editing anything in this repo.
---

# Just Move the Button — working on this project

An interactive comic (guess → reveal, one page at a time) that shows non-technical people the invisible work behind a "simple" software change. Comic-book style: bold ink, halftone, captions, SFX, splash panels. The reader picks a hero and follows their bad Tuesday.

## Layout
```
index.html          dev shell (ES modules, relative assets) — open with any static server
src/tokens.css      ALL colours, type, rhythm, motion. Change the look here first.
src/comic.css       panel grammar: .panel .cap .sfx .bubble .think .inst … (no colours hardcoded)
src/heroes.js       hero manifest: name, tagline, card colour, asset paths
src/instruments.js  the things that snap: before/after HTML per instrument
src/story.js        the script: ISSUE + PAGES (all copy lives here, nowhere else)
src/engine.js       renders PAGES; knows nothing about the story content
assets/<hero>/      12 transparent PNGs per hero (see "Adding a hero")
tools/cut_sheets.py turns three Gemini sheets into the 12 PNGs
tools/build.py      bundles everything into dist/index.html (single shareable file)
dist/index.html     build output — do not edit by hand
docs/DESIGN.md      the visual rules and why
```

## Rules
1. **Copy lives in story.js only.** Never put reader-facing words in engine.js, comic.css, or instruments.js.
2. **Colours live in tokens.css only.** If you type a hex value anywhere else, stop.
3. **Engine is content-agnostic.** Adding a page must not require touching engine.js. If it does, the schema needs extending, not the page.
4. **Language: short sentences, no jargon.** A twelve-year-old should follow it. "Robot that reads the page", not "CI test suite".
5. **No named creatures.** The things that snap are described by what they do (the checker, the counter, the voice). Only heroes have names.
6. **Every guess page ends with one takeaway line** (`reveal.take`). One sentence. Quotable.
7. Rebuild after any change: `python3 tools/build.py` (add `--maxh 480` for a smaller file).
8. Smoke-test in a browser before sharing. There is a Playwright script pattern in git history; console must be empty.

## Page schema (story.js)
```js
{ id:'counter', type:'guess', title:'The Counter',
  p1:{ cap, pose, think, bg },              // hero panel. pose ∈ typing|phone|alarm|slumped. bg ∈ cyan|yel|mag|green|blue|paper
  p2:{ cap, inst, bg },                     // "meanwhile" panel. inst = key in instruments.js, shown in its BEFORE state
  q:{ text, choices:[..2-3..], answer:i },  // answer index; null = unscored (a question with no right answer)
  splash:{ cap, inst, sfx, pose, sub },     // inst shown in AFTER state; sfx is 1 word + punctuation; sub = bottom-right caption
  w:{ p1cap, chat:[{who:'me'|'them',text}], sub, text },  // ticket-writer POV: replaces p1 (a phone chat), splash.sub and reveal.text. REQUIRED on every guess page.
  reveal:{ face, title, text, take } }      // face ∈ calm|thinking|worried|shocked|exhausted|relieved
```
Thought bubbles get a 'careful' variant automatically via CAREFUL in story.js — add a mapping there when you add a new `think`.

Other page types: `estimate` (first page; also reused as the last question) and `end`. Order in PAGES is the reading order.

## Cover / state
The cover collects: name (optional), role (`dev` | `writer`), mood (`confident` | `careful`), issue (ISSUES in story.js; only available ones are clickable). `state.role` drives which caption set renders. Hero selection returns automatically when a second hero has `available:true` — the engine currently hardcodes maya on start; swap to a picker in renderCover when Leo lands.

## Adding a page
1. If it needs a new instrument, add it to instruments.js: `{ before: html, after: html }`. Use existing `.inst` sub-classes (`.card .meter .say .screen .cal .btnui .stamp .env`) before inventing new CSS.
2. Add the page object to PAGES in story.js — including the `w` block. A page without a writer POV breaks writer mode. Escalate the hero: early pages `thinking/worried`, late pages `exhausted`, last page `relieved`.
3. `python3 tools/build.py`, open dist/index.html, click through.

## Adding a hero
1. Generate three sheets in Gemini with the prompts in docs/DESIGN.md "Hero prompts". White background, no text. Same style sentence every time.
2. `python3 tools/cut_sheets.py leo turnaround.jpg expressions.jpg poses.jpg` → writes assets/leo/*.png
3. In heroes.js set `available: true` and fill `art` with the 12 paths. Card colour: `card: 'mag'`.
4. Check the contact sheet: every face must have the same hair, glasses, and outfit. If one drifted, regenerate that sheet — don't keep it.

## Changing the look
- Palette, line weight, fonts, halftone density, motion timing: tokens.css.
- Panel shapes and components: comic.css. Keep the grammar names; other pages depend on them.
- Do not add a third font. Do not add rounded corners to panels. Do not soften the shadows. See DESIGN.md for why.

## Next issue plan
Issue #2: "Just add a phone number field." Same heroes, same instruments plus `form` and `analytics-dip`. Reader predicts *who snaps* before each page instead of *what happens* — the second-round mechanic. Ends with both scores side by side.
