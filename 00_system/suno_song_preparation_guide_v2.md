# SUNO Song Preparation Guide v2.0

## Purpose

This guide defines how agents must prepare input for SUNO.

It does not define musical taste, album philosophy, lyrical themes, artist identity, or fixed style libraries.

Its only purpose is to make sure every SUNO prompt is delivered in a clean, consistent, copyable format that SUNO can interpret well.

**Examples in this guide are illustrative only.** They span different genres and moods so you can see the *format*, not a default aesthetic. When preparing a real song, follow the user's `01_artist/artist_dna.md`, `01_artist/style_reference.md`, song brief, and album palette — not the examples here.

---

## Core Rule

Whenever an agent prepares a song for SUNO, the final answer must use this exact structure:

1. Lyrics
2. Styles
3. More options
4. Exclude styles
5. Vocal Gender
6. Weirdness %
7. Style influence %
8. Song Title

The fields must always be clearly separated.

Lyrics, Styles, Exclude styles, and Song Title must always be delivered inside fenced text blocks.

---

## Required Output Template

### Lyrics

```text
[Verse 1]
...

[Chorus]
...

[Verse 2]
...

[Bridge]
...

[Final Chorus]
...

[Outro]
...
```

### Styles

```text
...
```

### More options

### Exclude styles

```text
...
```

### Vocal Gender

M/F

### Weirdness %

0%

### Style influence %

50%

### Song Title

```text
...
```

---

## Field Rules

### 1. Lyrics

The Lyrics field must contain only the lyrics and SUNO-readable structural markers.

Allowed structural markers include:

```text
[Intro]
[Verse 1]
[Verse 2]
[Pre-Chorus]
[Chorus]
[Post-Chorus]
[Bridge]
[Breakdown]
[Instrumental]
[Spoken]
[Call and Response]
[Final Chorus]
[Outro]
[Fade Out]
```

Use structural markers to guide SUNO toward a song shape.

Do not include explanations, comments, production notes, or emotional analysis inside the Lyrics field.

Good:

```text
[Verse 1]
I woke up with the morning light
A quiet song inside my chest

[Chorus]
Let it rise
Let it rise
Something moving through my life
```

Bad:

```text
This song should feel emotional and start softly.
[Verse]
...
```

---

## Lyric Formatting Rules

### Keep lines singable

SUNO responds better to short, natural lines than long prose.

Prefer:

```text
I let go
I breathe in
I come back
To where I begin
```

Avoid:

```text
I suddenly realize that all the fear I carried was only a shadow created by my own mind
```

### Use repetition intentionally

Repetition helps SUNO create hooks, choruses, chant sections, and memorable phrasing.

Use repetition when the song needs:

- hook energy
- sing-along energy
- emphasis on a key phrase
- emotional release
- dance or groove stability

Example:

```text
I won't look back
I won't look back
I won't look back now
```

### Avoid overloading verses

If lyrics contain too many concepts, SUNO may flatten the delivery.

Use one central emotional movement per song.

### Use bridges for perspective shifts

The bridge should introduce a change:

- realization
- surrender
- lift
- confession
- turning point
- quiet breakdown
- final escalation

---

## SUNO Metadata Tags Inside Lyrics

SUNO may respond to performance and arrangement tags inside the Lyrics field, but they should be used sparingly.

Allowed examples:

```text
[Spoken]
[Softly]
[Whispered]
[Call and Response]
[Choir Response]
[Instrumental Break]
[Drum Break]
[Clapping]
[Harmonies]
[Final Chorus, bigger]
```

Do not overuse these tags.

Too many tags can confuse the model or make the result feel mechanical.

Use tags only when they help the musical form.

---

## 2. Styles

The Styles field must describe the sound SUNO should generate.

This field should use concrete musical keywords.

A strong style prompt usually includes:

- genre or hybrid genre
- rhythm or groove
- instrumentation
- vocal delivery
- production feel
- emotional tone
- era or recording texture, when useful
- energy arc, when useful

Example (folk / soul):

```text
warm acoustic folk, brushed drums, upright bass, intimate male vocal, close room mic, reflective verses with a fuller chorus, mid-tempo pocket groove
```

Example (indie rock):

```text
indie rock, crunchy rhythm guitar, live drum kit, melodic bass, raw female lead vocal, garage-room energy, tense verses and explosive chorus
```

Example (R&B / pop):

```text
modern R&B, warm synth pads, tight programmed drums, smooth bass, layered harmonies, polished but human vocal, late-night mood, slow build in the bridge
```

Pick the recipe that matches the song brief and the artist's style families — not a default genre from this guide.

---

## Style Prompt Principles

### Use concrete musical language

SUNO responds better to concrete words than abstract emotion alone.

Prefer:

```text
warm electric guitar, tight live drums, melodic bass, dry room vocal, mid-tempo groove
```

Avoid:

```text
deep cinematic emotional awakening energy
```

Abstract feeling may be included, but it should be supported by concrete musical terms.

Good:

```text
lo-fi hip-hop, dusty drum loop, muted Rhodes, soft male vocal, tape hiss, late-night and introspective
```

---

## Style Prompt Building Blocks

### Genre and rhythm

Useful examples (pick what fits the brief — not a fixed palette):

```text
acoustic folk
indie rock
alt-pop
modern R&B
synth-pop
lo-fi hip-hop
country ballad
punk rock
post-punk
dark ambient
cinematic pop
Latin groove
Afrobeat-inspired
straight 4/4 rock
half-time trap-adjacent (without trap drums in Styles — use excludes)
disco-funk bounce
80s new wave
90s boom-bap feel
```

### Instruments

Useful examples:

```text
acoustic guitar
electric guitar
synth pads
808-style sub (describe texture, not genre label alone)
piano
Rhodes
organ
strings
brass stabs
live drum kit
programmed drums
bass guitar
upright bass
hand claps
percussion loops
choir harmonies
ambient textures
```

### Vocal delivery

Useful examples:

```text
intimate close-mic vocal
powerful belted chorus
whispered verses
raspy rock vocal
smooth R&B vocal
detached cool vocal
group chant on chorus
call-and-response vocals
spoken-word verses
double-tracked harmonies
```

### Production feel

Useful examples:

```text
organic live band feel
dry garage-room mix
polished modern pop production
lo-fi tape warmth
minimal and sparse
wide cinematic mix
dirty analog saturation
clean punchy mix
bedroom recording intimacy
arena-scale chorus lift
```

### Energy arc

Useful examples:

```text
starts intimate and grows gradually
steady groove throughout
quiet verses with bigger choruses
slow build toward a final lift
repetition with rising intensity
drops to half-time in the bridge
```

---

## Avoid References SUNO Cannot Know

SUNO has **no access** to this repo, your artist name, album names, song titles, style-direction labels, or shorthand like "Family-like." Those belong in file headers, `style_directions.md`, and agent notes — **never inside fenced Lyrics, Styles, Exclude styles, or Song Title blocks** that get pasted or sent to the API.

If a phrase only makes sense because you know SUNO Album Studio, **translate it** into concrete musical language before it goes in a SUNO field.

### Artist and band names

Do not use living or recognizable artist names in SUNO prompts.

Avoid:

```text
Bob Marley style
Adele-like vocal
like Mumford & Sons
sounds like The Beatles
```

Use descriptive substitutes.

Instead of:

```text
Bob Marley style
```

Use:

```text
classic roots reggae, warm offbeat guitar, relaxed bass groove, group call-and-response vocals, organic live band feel
```

Instead of:

```text
Adele-like vocal
```

Use:

```text
powerful soulful female vocal, emotional phrasing, piano-led arrangement, spacious modern ballad production
```

### Studio, album, and internal shorthand

Do not use names or labels from this project (or any project) as style shortcuts.

Avoid in **Styles** (and other SUNO fields):

```text
studio warmth shorthand
Family-like groove
Project-name percussion
Direction C
same as Track Title From Last Album
roots like [other album name]
```

Use the **translated musical recipe** instead. Write what those labels *mean* in sound:

| Internal shorthand (file headers only) | Put this in Styles instead |
|----------------------------------------|----------------------------|
| _[Family A — e.g. close acoustic]_ | fingerpicked guitar, close room mic, soft percussion, intimate vocal, gentle pulse, tape warmth |
| _[Family B — e.g. live band]_ | live drums forward, warm bass, rhythm guitar, room ambience, pocket groove, direct vocal |
| _[Artist DNA tag from style reference]_ | translate to instruments, vocal, production, and groove — never paste the label itself |

**Where studio context belongs:** HTML comment at top of `suno_prompt_vN.md`, `style_directions.md`, change logs, listening notes — not inside fenced blocks.

**Pre-flight:** Read the Styles block as if you know nothing about SUNO Album Studio. If a phrase requires repo context to mean anything, rewrite it.

---

## Positive Prompting Over Negative Prompting

SUNO is more reliable when told what to do than what not to do.

Prefer positive direction in Styles.

Weak:

```text
no EDM, no trap drums, no heavy autotune
```

Better:

```text
organic acoustic arrangement, natural vocal delivery, live percussion, warm analog texture
```

Use the Exclude styles field for strong exclusions, but do not rely on it alone.

---

## 3. More options

The More options section must always include:

- Exclude styles
- Vocal Gender
- Weirdness %
- Style influence %

These values should be chosen intentionally, not randomly.

---

## 4. Exclude styles

The Exclude styles field must contain only styles or sonic traits that should be avoided.

It must be delivered as a fenced text block.

Example:

```text
EDM, trap, metal, distorted guitars, heavy autotune, cinematic trailer music, orchestral bombast
```

Keep exclusions concise.

Do not write full sentences.

Good:

```text
EDM, trap drums, heavy autotune, metal, harsh synths
```

Bad:

```text
Do not make this sound like modern EDM and please avoid anything too dramatic or artificial.
```

---

## 5. Vocal Gender

Use only:

```text
M
```

or

```text
F
```

If the user has not specified a gender, choose the gender that best supports the song and matches `01_artist/artist_identity.md` when available.

For group songs, choose the lead vocal gender and describe the group vocals in Styles.

Example:

```text
Vocal Gender

M
```

Styles:

```text
male lead vocal with stacked gang vocals on the chorus
```

---

## 6. Weirdness %

Weirdness controls how unusual or unexpected the generation may become.

Use it carefully.

### Recommended ranges

```text
0–10%   very safe, conventional, predictable
10–25%  natural variation, still stable
25–40%  more surprising phrasing or arrangement choices
40–60%  experimental, higher risk
60%+    only for deliberate weirdness
```

### Default recommendation

For most serious songs:

```text
15%
```

For repetition-heavy, playful, or experimental songs:

```text
25–40%
```

For album-consistent songs (tight cohesion across tracks):

```text
10–20%
```

For commercial or release-ready songs:

```text
10–15%
```

---

## 7. Style influence %

Style influence controls how strongly SUNO should follow the Styles field.

### Recommended ranges

```text
20–35%  loose interpretation, more model freedom
40–60%  balanced control, recommended default
60–80%  strong adherence to style prompt
80%+    rigid style control, may reduce naturalness
```

### Default recommendation

For most songs:

```text
55%
```

For very specific style goals:

```text
65–75%
```

For open exploration:

```text
35–45%
```

For album consistency:

```text
60–70%
```

---

## 8. Song Title

The Song Title field must contain only the title inside a fenced text block.

Example:

```text
Every Step Is a Choice
```

Avoid subtitles unless the user explicitly wants them.

---

## Agent Behavior Rules

### Always output SUNO input cleanly

When the user asks for a SUNO-ready song, the agent must provide the template only.

No explanations before or after unless the user asks for reasoning.

### Do not mix instructions into SUNO fields

Do not write:

```text
This should be sung softly.
```

inside Lyrics.

Put delivery and sound direction in Styles.

### Do not invent unnecessary style systems

This guide does not contain a fixed style library.

The agent may create a style prompt based on the user's intent, song brief, and artist style reference — but it must describe the sound concretely.

### Preserve user lyrics when requested

If the user provides lyrics and asks only for formatting, do not rewrite the lyrics unless asked.

### Improve silently when appropriate

If user lyrics are too long, unsingable, or structurally unclear, the agent may lightly shape them into SUNO-friendly form while preserving the meaning.

### Ask only when required

If the song can be completed with reasonable assumptions, complete it.

Do not block the workflow with unnecessary questions.

---

## SUNO-Specific Best Practices

### Separate lyrics from style

Lyrics should tell SUNO what is sung.

Styles should tell SUNO how it sounds.

Do not overload lyrics with production direction.

### Use structure tags

Structure tags help SUNO understand song sections.

Use them consistently.

### Keep choruses clear

The chorus should be the emotional center.

It should be shorter, more repeated, and more memorable than the verses.

### Use hooks

A hook can be:

- a repeated phrase
- a chant or slogan
- a question
- a short declaration
- a rhythmically satisfying line

Example:

```text
Don't wait up
Don't wait up
I'm already gone
```

### Keep style prompts compact

A good style prompt is usually one compact paragraph.

Do not write a long essay in the Styles field.

### Combine styles carefully

SUNO can blend genres, but too many competing styles can weaken the result.

Good:

```text
indie rock with synth bass and stacked gang vocals on the chorus
```

Risky:

```text
indie rock, techno, medieval folk, flamenco, cinematic orchestral, punk, ambient jazz
```

### Use one rhythmic center

Every prompt should imply one main groove.

Examples:

```text
mid-tempo 4/4 rock groove
syncopated funk pocket
half-time trap-adjacent swing (describe drums, not genre alone)
slow ballad sway
four-on-the-floor dance pulse
driving punk downstrokes
```

### Use one emotional center

Every song should have one main emotional direction.

Examples:

```text
defiant and restless
joyful and communal
quiet and reflective
tense and unresolved
playful and bright
melancholic but tender
cold and detached
```

---

## Recommended Defaults

When the user gives no technical preferences, use values that match the song brief and `01_artist/style_reference.md` when available. If nothing else is known:

```text
Vocal Gender

M or F — whichever fits the brief and artist identity
```

```text
Weirdness %

15%
```

```text
Style influence %

55%
```

When the brief calls for tight control (release-ready, album cohesion, minimal surprise):

```text
Weirdness %

10–20%
```

```text
Style influence %

60–70%
```

Use higher Style influence when consistency matters across an album. Use lower Weirdness for precision; raise it when the brief asks for surprise or experimentation.

---

## Output Example

Illustrative only — an indie-pop song shape. Replace content with the user's lyrics, style families, and brief.

### Lyrics

```text
[Verse 1]
I was walking through the city
With a weight I couldn't name
Then the noise fell away for a second
And I knew I couldn't stay the same

[Chorus]
I'm not going back
I'm not going back
I'm not going back to before

[Verse 2]
Every version that I tried to be
Was someone else's open door
I'm done performing what they wanted
I know what I'm fighting for

[Chorus]
I'm not going back
I'm not going back
I'm not going back to before

[Bridge]
Let the old story end right here

[Final Chorus]
I'm not going back
I'm not going back
I'm not going back to before

[Outro]
Not going back
Not going back
```

### Styles

```text
indie pop, jangly electric guitar, live drums with tight snare, melodic bass, stacked female lead vocal with doubles on chorus, bright room mix, defiant and forward-moving, verses lean and chorus opens wide
```

### More options

### Exclude styles

```text
EDM, trap, metal, heavy autotune, harsh synths, cinematic trailer music
```

### Vocal Gender

F

### Weirdness %

15%

### Style influence %

60%

### Song Title

```text
Not Going Back
```

---

## Final Instruction For Agents

Whenever preparing SUNO input, deliver clean copy-ready blocks in the required format.

Do not include commentary inside the SUNO fields.

Do not rely on artist references.

Use concrete musical language matched to the user's brief and artist files — not a default genre from this guide.

Use structure tags.

Choose Weirdness and Style influence intentionally.

Always make the output easy to copy directly into SUNO.