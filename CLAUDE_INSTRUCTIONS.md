# Claude Cowork Instructions — Dead in the Region Podcast Production

These instructions tell a Claude Cowork session how to use the files in this repository to generate podcast episodes in Speechify Studio.

---

## Repository Structure

```
dead-in-the-region-editor/
├── app.py                              # Streamlit app — Episode Editor (main page)
├── helpers.py                          # Shared utilities for GitHub commits, data loading
├── pages/
│   ├── 1_🎙️_Speaker_Profiles.py      # Speaker profile editor page
│   └── 2_👥_Audience_and_Mood.py      # Audience & mood settings page
├── data/
│   ├── episodes.csv                    # 12-episode season guide (all episode metadata)
│   ├── speakers.json                   # Speaker profiles: name, biography, voice_style
│   └── audience.json                   # Audience & mood templates for Speechify Step 2
├── prompts/
│   └── ep01-the-borman-lights.md       # Generated prompt files (one per episode)
│   └── ...                             # More prompt files as they're generated
├── CLAUDE_INSTRUCTIONS.md              # THIS FILE — instructions for Claude Cowork
└── requirements.txt                    # Python dependencies
```

---

## What Each File Contains

### `data/speakers.json`
Contains three speaker profiles (Nate Alderman, Carmen Reyes, Dr. Mara Vasquez). Each has:
- `name` — paste into Speechify's Name field
- `biography` — paste into Speechify's Biography field
- `voice_style` — paste into Speechify's Voice Style field
- `type` — "host" or "guest" (determines Speechify speaker slot)
- `episodes` — which episodes this speaker appears in

### `data/audience.json`
Contains five audience/mood text blocks that stay the same for every episode:
- `primary_audience` — paste into Speechify Step 2, "Primary Audience"
- `geography_background` — paste into Speechify Step 2, "Geography & Background"
- `values_interests` — paste into Speechify Step 2, "Values & Interests"
- `mood` — paste into Speechify Step 2, "Mood"
- `tone` — paste into Speechify Step 2, "Tone"

### `prompts/ep##-title-slug.md`
Per-episode prompt files generated from the CSV. Each contains the full creative prompt to paste into Speechify's "Text Idea" field in the Pre-Creation Dialog. Sections include:
- PODCAST header (title, format, type, hosts, speakers)
- COLD OPEN
- THE CASE
- HOST DYNAMICS
- TONAL MAP
- HORROR/ATMOSPHERE BEATS
- DARK HUMOR BEATS
- SERIALIZATION NOTES
- NEXT EPISODE TEASE
- PRODUCTION NOTES

### `data/episodes.csv`
The master episode guide with 21 columns per episode. The Streamlit app and prompt generator both read from this file.

---

## How to Generate a Podcast Episode in Speechify Studio

### Prerequisites
- Have the Speechify Studio tab open (https://studio.speechify.com)
- Have access to this repository (either cloned locally or via the Streamlit app at https://dead-in-the-region-editor-fmmnhnuxkjvxqtl4jvplrr.streamlit.app/)

### Step-by-Step Process

#### Step 0: Gather Materials
1. Read the prompt file for the episode you want to generate: `prompts/ep##-title.md`
2. Read `data/speakers.json` to get the speaker profiles
3. Read `data/audience.json` to get the audience/mood templates
4. Note the episode's speaker count (from the prompt file header — SPEAKERS: 2 or 3)

#### Step 1: Create the Podcast in Speechify
1. Navigate to Speechify Studio → Library
2. Click **"Create a Podcast (Beta)"** (or the podcast creation button)
3. In the Pre-Creation Dialog:
   - Select the **"Text Idea"** tab
   - Paste the ENTIRE contents of the episode's prompt file (`prompts/ep##-title.md`)
   - Set **Language** to "English (US)"
   - Set **Number of Speakers** to 2 (or 3 if the prompt says SPEAKERS: 3)
   - Set **Duration** to "20-30min"
4. Click **"Create"**

#### Step 2: Review Source Content (Speechify Step 1)
Speechify generates a research document from the prompt. Review it:
- Does it follow the cold open instructions?
- Are the three acts clearly structured?
- Are NWI geography details specific?
- Are horror and humor beats present?
- Are foundry/serialization elements included?

If it drifted, use the chat refinement input to redirect. If seriously off, click Regenerate.

Click **"Next step"** when satisfied.

#### Step 3: Set Audience & Mood (Speechify Step 2)
Speechify generates audience targeting. **Replace all fields** with the templates from `data/audience.json`:

1. Clear the "Primary Audience" textarea → paste `audience.primary_audience`
2. Clear "Geography & Background" → paste `audience.geography_background`
3. Clear "Values & Interests" → paste `audience.values_interests`
4. Clear "Mood" → paste `audience.mood`
5. Clear "Tone" → paste `audience.tone`

**Episode-specific overrides:**
- Episode 8 (Tape 7, format-breaker): Adjust Mood to emphasize found-footage atmosphere, reduce humor references
- Episode 11 (Meridian Line Pt 3, climax): Adjust Mood to emphasize building dread and emotional intensity
- Episode 12 (Signal and Noise, finale): Adjust Tone to note warmer, more reflective register

Click **"Next step"** when done.

#### Step 4: Set Speaker Profiles (Speechify Step 3)
Speechify generates speaker names/bios/voices. **Replace all fields** with profiles from `data/speakers.json`:

**For 2-speaker episodes (standard):**
- Speaker 1 (Host): Name = "Nate Alderman", Biography = Nate's `biography`, Voice Style = Nate's `voice_style`
- Speaker 2 (Guest): Name = "Carmen Reyes", Biography = Carmen's `biography`, Voice Style = Carmen's `voice_style`

**For 3-speaker episodes (Episodes 6, 8, 10, 12 with Dr. Vasquez):**
- Speaker 1 (Host): Nate Alderman (full profile)
- Speaker 2 (Guest 1): Carmen Reyes (full profile)
- Speaker 3 (Guest 2): Dr. Mara Vasquez (full profile)

**Episode-specific notes:**
- Episode 8 (format-breaker): May need an additional "Unidentified Explorer" speaker for the found-tape sections
- Add episode-specific voice notes when needed, e.g.: "In this episode, Carmen is more subdued than usual"

Click **"Next step"** when done.

#### Step 5: Review Script (Speechify Step 4)
Speechify generates the full dialogue. Review checklist:
- [ ] Cold open hooks immediately (first 30 seconds compelling without context)
- [ ] Host voices are distinct (Nate sounds like Nate, Carmen sounds like Carmen)
- [ ] Comedy/horror balance works (humor after tension, not during victim sections)
- [ ] Sound design cues included ([pause], [laughter], ambient descriptions)
- [ ] Act structure is clear (setup → investigation → turn → outro)
- [ ] Foundry/arc references present (per the prompt's SERIALIZATION NOTES)
- [ ] Callbacks work (listeners who missed earlier episodes shouldn't be lost)
- [ ] Episode ends with a hook (tease from NEXT EPISODE TEASE section)

Use chat refinement for targeted fixes. Edit directly for small changes.

Click **"Next step"** to generate audio.

#### Step 6: Audio Generation & Export
Audio generates block by block (takes several minutes). When complete:
- Spot-check: cold open, one mid-episode section, and the outro
- Verify host voices sound distinct
- Check that tonal shifts land
- Export via the Export button

---

## Speechify Field Map (Quick Reference)

| Speechify Location | What to Paste | Source File |
|---|---|---|
| Pre-Creation → Text Idea | Full episode prompt | `prompts/ep##-title.md` |
| Pre-Creation → Language | English (US) | Fixed |
| Pre-Creation → Speakers | 2 or 3 | From prompt header |
| Pre-Creation → Duration | 20-30min | Fixed |
| Step 2 → Primary Audience | Audience template | `data/audience.json` → `primary_audience` |
| Step 2 → Geography | Geography template | `data/audience.json` → `geography_background` |
| Step 2 → Values & Interests | Values template | `data/audience.json` → `values_interests` |
| Step 2 → Mood | Mood template | `data/audience.json` → `mood` |
| Step 2 → Tone | Tone template | `data/audience.json` → `tone` |
| Step 3 → Host Name | "Nate Alderman" | `data/speakers.json` → speakers[0].name |
| Step 3 → Host Biography | Nate's bio | `data/speakers.json` → speakers[0].biography |
| Step 3 → Host Voice Style | Nate's voice | `data/speakers.json` → speakers[0].voice_style |
| Step 3 → Guest 1 Name | "Carmen Reyes" | `data/speakers.json` → speakers[1].name |
| Step 3 → Guest 1 Biography | Carmen's bio | `data/speakers.json` → speakers[1].biography |
| Step 3 → Guest 1 Voice Style | Carmen's voice | `data/speakers.json` → speakers[1].voice_style |
| Step 3 → Guest 2 Name | "Dr. Mara Vasquez" | `data/speakers.json` → speakers[2].name |
| Step 3 → Guest 2 Biography | Vasquez's bio | `data/speakers.json` → speakers[2].biography |
| Step 3 → Guest 2 Voice Style | Vasquez's voice | `data/speakers.json` → speakers[2].voice_style |

---

## Episode Production Order

Generate episodes in order (1 through 12) to maintain continuity. Each episode should be reviewed before generating the next, as adjustments to voice style or audience settings based on output quality should be saved back to the JSON files.

| Ep | Title | Speakers | Prompt File |
|---|---|---|---|
| 1 | The Borman Lights | 2 | `prompts/ep01-the-borman-lights.md` |
| 2 | Bodies in the Basement | 2 | `prompts/ep02-bodies-in-the-basement.md` |
| 3 | Shotgun Peterson | 2 | `prompts/ep03-shotgun-peterson.md` |
| 4 | The Whiting Recordings Pt 1 | 2 | `prompts/ep04-the-whiting-recordings-part-1.md` |
| 5 | The Whiting Recordings Pt 2 | 2 | `prompts/ep05-the-whiting-recordings-part-2.md` |
| 6 | Belle Gunness | 3 | `prompts/ep06-belle-gunness--la-portes-lady-bluebeard.md` |
| 7 | The Lake Effect | 2 | `prompts/ep07-the-lake-effect.md` |
| 8 | Tape 7 | 3 | `prompts/ep08-tape-7.md` |
| 9 | The Meridian Line Pt 1 | 2 | `prompts/ep09-the-meridian-line-part-1.md` |
| 10 | The Meridian Line Pt 2 | 3 | `prompts/ep10-the-meridian-line-part-2.md` |
| 11 | The Meridian Line Pt 3 | 2 | `prompts/ep11-the-meridian-line-part-3.md` |
| 12 | Signal and Noise | 3 | `prompts/ep12-signal-and-noise-season-finale.md` |

---

## Notes for Claude Cowork Browser Automation

When automating Speechify via Claude Cowork's browser tools:

1. **Reading files:** Use the GitHub raw content URLs or clone the repo locally. All data files are JSON or Markdown — easy to parse.

2. **Pasting into Speechify:** Speechify uses rich-text editors. When pasting, you may need to:
   - Click into the textarea to focus it
   - Select all existing text (Ctrl+A / Cmd+A) to clear the generated content
   - Paste the new content (Ctrl+V / Cmd+V)
   - Wait for any auto-save or validation to complete before moving to the next field

3. **Navigation:** Speechify's podcast creation wizard has clear "Next step" buttons. Navigate sequentially through all steps.

4. **Field detection:** Use the accessibility tree or `find` tool to locate text areas. The fields are labeled (e.g., "Primary Audience", "Biography", "Voice Style") and can be found by their labels.

5. **Long text fields:** Speaker biographies and voice styles are 100-200 words each. Make sure the full text is pasted (don't truncate). The audience fields are similarly sized.

6. **Multi-step workflow:** The production of one episode touches 15+ fields across 4 wizard steps. Work through them methodically. Don't skip steps.

7. **Prompt file access:** If the prompt files haven't been generated yet, use the Streamlit app's "Generate All Prompts" button first, or generate them one at a time from the Episode Editor.
