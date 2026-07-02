# SUNO Song Preparation Guide v2.0

## Purpose

This guide defines how ChatGPT must prepare input for SUNO.

It does not define musical taste, album philosophy, lyrical themes, artist identity, or fixed style libraries.

Its only purpose is to make sure every SUNO prompt is delivered in a clean, consistent, copyable format that SUNO can interpret well.

---

## Core Rule

Whenever ChatGPT prepares a song for SUNO, the final answer must use this exact structure:

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
Love is moving through my life
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
I come home
To the light within
```

Avoid:

```text
I suddenly realize that all the fear I carried was only a shadow created by my own mind
```

### Use repetition intentionally

Repetition helps SUNO create hooks, mantras, choruses, and memorable phrasing.

Use repetition when the song needs:

- mantra energy
- sing-along energy
- spiritual emphasis
- emotional release
- dance or groove stability

Example:

```text
I let love lead me
I let love lead me
I let love lead me home
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
- final awakening

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

Example:

```text
roots reggae with warm acoustic guitar, relaxed offbeat rhythm, soft bass groove, hand claps, small gospel choir responses, sincere male vocal, organic live band feel, hopeful and grounded, gradual uplifting chorus
```

---

## Style Prompt Principles

### Use concrete musical language

SUNO responds better to concrete words than abstract emotion alone.

Prefer:

```text
warm acoustic guitar, hand claps, upright bass, soft gospel choir, relaxed reggae groove
```

Avoid:

```text
deep spiritual awakening energy
```

Abstract feeling may be included, but it should be supported by concrete musical terms.

Good:

```text
warm acoustic folk, gentle fingerpicked guitar, soft male vocal, intimate room sound, reflective and hopeful
```

---

## Style Prompt Building Blocks

### Genre and rhythm

Useful examples:

```text
roots reggae
light reggae bounce
acoustic folk
soulful pop
gospel-inspired
tribal percussion
world folk
70s singer-songwriter
island groove
nyabinghi-inspired rhythm
soft rock
cinematic acoustic
ambient pop
```

### Instruments

Useful examples:

```text
acoustic guitar
ukulele
warm bass
upright bass
organ
piano
hand claps
tambourine
soft percussion
congas
shakers
nyabinghi drums
choir harmonies
brass accents
strings
ambient pads
```

### Vocal delivery

Useful examples:

```text
sincere male vocal
gentle female vocal
warm group vocals
call-and-response vocals
small gospel choir
soft spoken verses
uplifting chorus vocals
raw emotional lead vocal
calm intimate vocal
```

### Production feel

Useful examples:

```text
organic live band feel
warm analog texture
minimal production
roomy acoustic sound
vintage tape warmth
clean modern mix
small stage performance
campfire sing-along feel
open-air live recording feel
```

### Energy arc

Useful examples:

```text
starts intimate and grows gradually
steady groove throughout
quiet verses with uplifting choruses
slow build toward a joyful final chorus
mantra-like repetition with rising energy
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
classic roots reggae, warm offbeat guitar, relaxed bass groove, spiritual group vocals, organic live band feel
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
| Intimate Acoustic family | fingerpicked nylon guitar, close room mic, soft brushed drums, warm vocal, gentle pulse, tape warmth |
| Live Band Pulse family | live drums forward, warm electric bass, rhythm guitar, room ambience, pocket groove, sincere vocal |
| Artist DNA / warmth | organic live band feel, analog tape warmth, human timing, warm sincere vocal, discovered performance not overproduced |

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

If the user has not specified a gender, choose the gender that best supports the song.

For group songs, choose the lead vocal gender and describe the group vocals in Styles.

Example:

```text
Vocal Gender

M
```

Styles:

```text
warm male lead vocal with mixed group choir responses
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

For mantra, tribal, playful, or experimental songs:

```text
25–40%
```

For album-consistent emotional songs:

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

## ChatGPT Behavior Rules

### Always output SUNO input cleanly

When the user asks for a SUNO-ready song, ChatGPT must provide the template only.

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

ChatGPT may create a style prompt based on the user’s intent, but it must describe the sound concretely.

### Preserve user lyrics when requested

If the user provides lyrics and asks only for formatting, do not rewrite the lyrics unless asked.

### Improve silently when appropriate

If user lyrics are too long, unsingable, or structurally unclear, ChatGPT may lightly shape them into SUNO-friendly form while preserving the meaning.

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
- a mantra
- a question
- a short declaration
- a rhythmically satisfying line

Example:

```text
Love in my heart
Peace in my mind
Light in my body
One step at a time
```

### Keep style prompts compact

A good style prompt is usually one compact paragraph.

Do not write a long essay in the Styles field.

### Combine styles carefully

SUNO can blend genres, but too many competing styles can weaken the result.

Good:

```text
roots reggae with gospel choir responses and acoustic folk warmth
```

Risky:

```text
roots reggae, techno, medieval folk, flamenco, cinematic orchestral, punk, ambient jazz
```

### Use one rhythmic center

Every prompt should imply one main groove.

Examples:

```text
relaxed offbeat reggae groove
steady tribal percussion
slow gospel sway
gentle acoustic folk pulse
mid-tempo soul groove
```

### Use one emotional center

Every song should have one main emotional direction.

Examples:

```text
hopeful and grounded
joyful and communal
quiet and reflective
reverent but warm
playful and bright
melancholic but healing
```

---

## Recommended Defaults

When the user gives no technical preferences, use:

```text
Vocal Gender

M
```

```text
Weirdness %

15%
```

```text
Style influence %

55%
```

For calm or healing-oriented songs, common defaults are:

```text
Weirdness %

15–25%
```

```text
Style influence %

60–70%
```

Use higher Style influence when consistency matters across an album.

---

## Output Example

### Lyrics

```text
[Verse 1]
I was walking through the morning
With a shadow in my chest
Then the light came through the window
And my heart began to rest

[Chorus]
Love in my heart
Peace in my mind
I take one step
One step at a time

[Verse 2]
I was holding on to worry
Like a stone inside my hand
Then I opened up my fingers
And I finally understand

[Chorus]
Love in my heart
Peace in my mind
I take one step
One step at a time

[Bridge]
I do not need to carry
What was never mine to hold

[Final Chorus]
Love in my heart
Peace in my mind
I take one step
One step at a time

[Outro]
One step
One step
One step at a time
```

### Styles

```text
warm acoustic roots reggae, relaxed offbeat guitar, soft bass groove, hand claps, small gospel choir responses, sincere male lead vocal, organic live band feel, hopeful and grounded, quiet verses with uplifting choruses
```

### More options

### Exclude styles

```text
EDM, trap, metal, heavy autotune, harsh synths, cinematic trailer music
```

### Vocal Gender

M

### Weirdness %

15%

### Style influence %

65%

### Song Title

```text
One Step at a Time
```

---

## Final Instruction For ChatGPT

Whenever preparing SUNO input, deliver clean copy-ready blocks in the required format.

Do not include commentary inside the SUNO fields.

Do not rely on artist references.

Use concrete musical language.

Use structure tags.

Choose Weirdness and Style influence intentionally.

Always make the output easy to copy directly into SUNO.