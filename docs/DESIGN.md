# Design system

## The idea
A Marvel-era comic page, drawn about something boring on purpose. The drama is in the framing, not the subject. Every snapped wire gets a splash panel. By page 7 the reader has a stack of SNAP!s behind them — that stack is the argument.

## Tokens (src/tokens.css)
- **Ink** `#111` for every line, shadow, and text. Never grey lines.
- **Paper** `#F3EBD6` newsprint. Halftone dots at 5px on the page, 7px inside panels.
- **Primaries** yellow / red / blue / cyan / magenta / green. Panel backgrounds are one flat primary + halftone. Never gradients.
- **Line** 4px panels, 3px captions. Hard offset shadows (`5px 5px 0 ink`), never blur.
- **Type** Bangers for anything shouted (titles, SFX, buttons, stamps). Barlow Semi Condensed 600/800 for everything read. Captions are uppercase. Two fonts, no more.
- **Motion** One easing for pops (`cubic-bezier(.2,1.6,.4,1)`). Panels fade in staggered 400ms. The splash: burst → giant effect → SFX → hero, in that order, over ~1.5s. Respects reduced-motion.

## Cover
A real comic cover: red halftone field, tilted title in yellow, the hero mid-alarm, one shouted line. Below it the setup form — name, role, mood, issue — styled as the same chunky option blocks as the choices, so it reads as part of the comic, not a settings screen. One big button.

## Two points of view
The same seven pages are written twice. **Developer**: you did the thing, the hero panel shows you working, captions say what you did. **Ticket writer**: you sent the note and went to lunch; the hero panel is a phone chat, captions say what you're told (and not told). The instruments, questions and answers are identical — only who you are changes. The writer version is the one that lands with non-technical readers: nothing they did was careless, and seven things broke anyway.

## Page grammar
Every guess page is the same four panels + reveal. Readers learn the rhythm on page 1 and stop reading the UI.
1. **Hero panel** (top-left): what you did. Hero pose + thought bubble + yellow caption.
2. **Meanwhile panel** (top-right): the thing that will snap, in its before state. Caption starts "Meanwhile…" or names where it is.
3. **Question panel** (full width): speech bubble + three chunky choices A/B/C.
4. **Splash** (hidden until the reader answers — never show the consequence before the guess; full width, tilted −1°, black with red halftone): the after state, a yellow burst, one SFX word, the hero reacting, a bottom-right caption with the consequence in one line.
5. **Reveal box**: hero face + "You called it / Not quite" + one bold sentence + two plain sentences + a takeaway line with a yellow bar.

## Questions
Every question must be answerable from what is on the page. The reader should be able to *work it out*, not just guess — put the facts needed (dates, what the thing listens for, who reads what when) in the two setup panels. A guess with no clues is a coin flip and feels unfair.

## Captions
Yellow = narration. White = quoted speech (the ticket). Uppercase, ≤ 14 words. Top-left is setup, bottom-right is consequence.

## SFX
One word, one punctuation mark, red with black stroke, rotated 8°. It names the sound of the failure: HALT! SNAP! KRRK! DING! Never explain the SFX.

## Instruments
Drawn with CSS, not images, so they're crisp and themeable: meter, calendar, checker card, screen, speech bubble, button. Before state is calm and complete. After state changes ONE thing (needle drops, word clips, page mirrors) plus a red stamp. Don't add a second change — one is legible, two is noise.

## Heroes
AI-generated in Gemini from a fixed style sentence, cut with tools/cut_sheets.py. Flat cel colours, bold ink, light halftone — same grammar as the page so they sit in it. Twelve assets each: 2 standing, 6 faces, 4 poses. Faces escalate across the issue; the last page is the only relieved one.

### Hero prompts
Canon: *Character design sheet for an original comic book character. [description]. Style: American comic book illustration, bold black ink outlines, flat cel-shaded colours, halftone dot shading, confident expressive linework. Full body, standing, front view and three-quarter view side by side. Plain white background. No text, no logos, no props, no scene.*
Expressions (attach canon): *Same character as the attached reference image, identical face, hair and outfit. Expression sheet: six head-and-shoulders portraits in a 3×2 grid, same size, plain white background: 1 calm and confident, 2 thinking, 3 slightly worried, 4 shocked with wide eyes, 5 exhausted and defeated, 6 relieved and smiling. [same style sentence]. No text.*
Poses (attach canon): *Same character…, four full-body poses on a plain white background, side by side: 1 sitting at a desk typing on a laptop, 2 holding a phone looking at it, 3 standing with arms thrown up in alarm, 4 slumped in a chair. [same style sentence]. No text.*
Never say "Marvel" in a prompt.

## What not to do
Rounded panel corners, soft shadows, gradients, a third font, grey outlines, named mascots for the instruments, more than one change per splash, explaining a joke in a caption.
