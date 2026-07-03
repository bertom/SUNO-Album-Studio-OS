# First run — onboarding

**Once:** copy the prompt below into a new Cursor chat. The agent interviews you and fills `01_artist/` with your DNA.

**After that:** you never need this prompt again. Open a chat and start with a sentence — e.g. *"I've got an idea for a song — let's brainstorm."* The agent guides you through the creative workflow (brief → lyrics → style → SUNO → listen → final), switching **specialized studio roles** as the work needs it. Slash commands like `/lyrics` focus a step when you want; plain language works too.

---

**Copy from here ↓**

I'm setting up my SUNO Album Studio for the first time.

Run `/onboard artist` and interview me. Start with these questions one at a time:
1. What's your artist or project name?
2. In one sentence — what is your music about?
3. Name 3 things every song of yours must have.
4. Name 3 things you never want in your music.
5. Describe your ideal lead vocal.
6. Describe 2–3 "groove families" you love (how it moves, not Spotify genre labels).
7. Do you have existing SUNO songs or albums to archive? (yes/no — if yes we'll use `/backfill catalog` later)

When done, summarize what you wrote and tell me the next step: `/album seed` or drop notes in `02_albums/_album_template/input/` and `/orchestrate album`.

---

## After onboarding — example openers

- *"I've got an idea for a song — let's brainstorm."*
- *"Help me write lyrics for a track about …"*
- *"I copied `_album_template` to `my-album/` — let's orchestrate from what's in `input/`."*
- *"Run 3 had the right groove but the vocal is off — help me retry."*

See [USER_GUIDE.md](USER_GUIDE.md) for the full manual.
