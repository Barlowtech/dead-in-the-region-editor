---
name: ditr-scriptwriter
description: >
  Generate narrative podcast scripts for "Dead in the Region" from structured episode data.
  Takes episode metadata from a CSV (or the Streamlit Production Hub), combines it with speaker
  profiles and audience/mood settings, and writes a dialogue-ready script that Speechify Studio
  can flesh out into a full episode. The script follows a chronological narrative arc — not a
  production document — so Speechify treats it as a story to perform rather than notes to interpret.
  Use this skill whenever the user says "write a script", "generate a script", "scriptwrite",
  "draft episode", "write episode [N]", "script for Speechify", or any request to turn the
  episode data into something Speechify can voice. Also trigger when the user wants to preview
  what an episode would sound like before sending it to Speechify, or wants to adjust the
  narrative structure of an episode.
---

# Dead in the Region — Scriptwriter

Turn structured episode data into narrative podcast scripts ready for Speechify Studio.

## Why This Skill Exists

Speechify Studio is a voice performance engine. When you give it production notes — section headers
like "THE CASE" and "SERIALIZATION NOTES" — it tends to produce something that sounds like a news
report or a true-crime explainer. That's not what Dead in the Region is.

This show is two friends telling each other stories in a parking lot next to a steel mill. The
narrative arc matters. The banter matters. The way Carmen's voice changes when a story gets to her
matters. None of that comes through when Speechify is working from a production document.

This skill writes an actual script — chronological, dialogue-driven, structured as a story with
rising tension — that Speechify can perform. The speaker profiles and audience/mood data still go
into Speechify's configuration fields separately (they shape the voice performance). But the
creative content Speechify receives is a script, not a set of notes.

## Reference Files

Read these as needed during the workflow:

| Reference File | When to Read |
|---|---|
| `references/script-structure.md` | Before writing any script — the act structure and scene template |
| `references/speechify-workflow.md` | When ready to deliver — how the script fits into Speechify's fields |

---

## The Show's DNA

Before writing anything, internalize these principles. They're the difference between a script
that sounds like Dead in the Region and one that sounds like a generic true-crime podcast.

### It's a Story, Not a Report

Every episode tells a story. It has a beginning, middle, and end. It has rising tension, a turn,
and a release. The hosts aren't presenting information — they're pulling the listener into a
narrative. Nate builds atmosphere. Carmen reacts honestly. The listener experiences the story
through their dynamic, not through a summary of facts.

### The Hosts Are the Show

The cases are compelling, but people listen for Nate and Carmen. Their banter, their disagreements,
their running jokes, the moments where the comedy drops and something real comes through — that's
the hook. Every script needs to breathe with their relationship. If you stripped out the case
entirely, the listener should still want to hang out with these two.

### Earned Tonal Shifts

The show moves between comedy, tension, horror, and warmth — but every shift has to be earned.
You don't jump from a joke to a scare. You build. Carmen's humor gradually fades as a story gets
darker. Nate's voice gets quieter when something disturbs him. The listener should feel the
temperature change, not get whiplash.

### Specificity Over Spectacle

The horror in this show comes from specific, grounded details — not from dramatic language or
shock value. "A car running with the door open and the radio tuned to static" is scarier than
"a terrifying disappearance." The Region itself (the refineries, the highways, the industrial
decay) provides the atmosphere. Let the geography do the work.

### Dialogue-Only Production

Speechify Studio generates spoken dialogue only — no sound effects, no ambient audio, no music.
Everything the listener "hears" must come through the hosts' words. Atmosphere is described,
not produced. A creaking door is Carmen saying "and then the door just... opened. On its own."
Not a stage direction.

---

## Inputs

The skill needs three data sources from the `dead-in-the-region-editor` repository:

### 1. Episode Data (`data/episodes.csv`)
The master episode guide. Each row is one episode with 21 columns including Synopsis, Case Hook,
Cold Open Concept, Host Dynamics, Horror Beats, Humor Beats, Tone Arc, Serialization Notes, etc.

### 2. Speaker Profiles (`data/speakers.json`)
Three speaker profiles with biography and voice_style fields. These go into Speechify's speaker
configuration separately — they're NOT pasted into the script. But the skill reads them to write
dialogue that matches each character's voice.

### 3. Audience & Mood (`data/audience.json`)
Five text blocks (primary_audience, geography_background, values_interests, mood, tone) that go
into Speechify's audience configuration separately. The skill reads these to calibrate the overall
tone of the script.

---

## Workflow

### Step 1: Load Episode Data

Read the target episode's row from `data/episodes.csv`. Also read `data/speakers.json` and
`data/audience.json` for voice and tone reference.

Identify:
- Which speakers appear (2 or 3? Is Dr. Vasquez in this episode?)
- Who tells the story (Told By field)
- Episode type (Real, Fictional, Mixed — affects how sourcing is handled)
- Format (Standalone, multi-part, format-breaker — affects structure)
- Position in season arc (early = light foundry seeds; late = direct foundry content)

### Step 2: Map the Narrative Arc

Before writing dialogue, map the episode's emotional journey using the Tone Arc field as a guide.
Read `references/script-structure.md` for the full act template.

The standard Dead in the Region episode follows this structure:

**COLD OPEN** (0:00–0:45)
A dialogue hook — the most compelling moment from the episode, dropped in without context.
Usually Carmen or Nate saying something that makes the listener need to know more.

**ACT 1: THE SETUP** (~0:45–8:00)
Banter. Personal moments. The hosts being themselves. The storyteller (Nate or Carmen) starts
setting up the case — where it happened, when, how they found it. The other host reacts, asks
questions, cracks jokes. Source attribution happens here ("I found this on Reddit" / "Court
transcripts from 1997"). The mood is warm and funny. The listener is settling in.

**ACT 2: THE CASE** (~8:00–20:00)
The story itself. Details accumulate. The humor starts thinning out as the case gets darker.
The non-storytelling host's reactions shift from jokes to genuine engagement. Horror beats land
through specific, grounded details described by the hosts. The foundry connection (if any) appears
as a detail within the story, not a separate section. By the end of Act 2, the mood has shifted
significantly from where it started.

**ACT 3: THE TURN** (~20:00–27:00)
The most intense or unsettling material. The moment that reframes everything. Comedy is gone or
nearly gone. Both hosts are fully in the story. If there's a cliffhanger (multi-part episodes),
it lands here. If standalone, this is where the case reaches its most disturbing or unresolved
point.

**OUTRO** (~27:00–30:00)
The hosts come back up for air. Process what they just discussed. Maybe a small joke to release
tension — but it should feel earned, not forced. Callbacks to previous episodes if relevant.
Next episode tease (usually Nate's line). Sign-off.

### Step 3: Write the Script

Write the script as a chronological dialogue document. Read `references/script-structure.md`
for the scene template and formatting rules.

**Formatting rules:**

Speaker labels in CAPS followed by a colon:
```
NATE: [dialogue]
CARMEN: [dialogue]
DR. VASQUEZ: [dialogue]
```

Parenthetical direction sparingly — only for significant tonal shifts:
```
CARMEN: (quieter now) I don't like this one.
NATE: (dry) You brought it.
CARMEN: I KNOW.
```

Scene breaks with a simple divider and a brief narrative stage direction:
```
---
[The mood shifts. Carmen's energy drops.]
---
```

**What to include:**
- All dialogue written out — this is the actual script Speechify will perform
- Brief narrative stage directions between scenes (in brackets) to signal tonal shifts
- Parenthetical emotion cues for moments where the voice needs to change significantly
- The cold open verbatim (or very close) from the CSV's Cold Open Concept field
- Personal moments and banter from the Host Dynamic fields, woven naturally into Act 1
- Horror beats from the CSV, translated into things the hosts SAY (not sound effects)
- Humor beats placed where the Tone Arc indicates comedy belongs
- Source attribution dialogue early in the episode
- Foundry/serialization details embedded in the story (not called out separately)
- Callbacks to previous episodes as natural dialogue, not exposition
- Next episode tease near the end

**What NOT to include:**
- Section headers like "ACT 1" or "THE CASE" — the script flows continuously
- Sound effect cues or ambient descriptions as stage directions
- Production notes or metadata — those go into Speechify's other fields
- Narration or voice-over — everything is dialogue between the hosts
- Explicit explanations of the foundry connection — let it emerge naturally

**Length target:** 4,000–6,000 words for a standard episode. This gives Speechify enough material
to generate 20-30 minutes of audio. Shorter for format-breakers (Episode 8). Longer for
multi-part finales.

**Voice consistency:** Every line should sound like the character speaking it. Reference the
speaker profiles:

- **Nate**: Deliberate, measured, builds atmosphere through specificity. Dry humor delivered flat.
  Gets quieter when disturbed. Cites sources naturally. Ohio transplant fascinated by NWI.
- **Carmen**: Fast, expressive, oral-tradition storytelling with digressions. Laughs freely.
  Gets conspiratorially quiet for dark humor. Goes genuinely silent when a story gets to her.
  NWI native, community knowledge, Reddit deep-dives.
- **Dr. Vasquez**: Academic precision with warmth. Slower pace, uses pauses before surprising facts.
  Dry humor more subtle than Carmen's. Conveys horror through restraint — the quieter she gets,
  the worse it is.

### Step 4: Self-Review

After writing, check:

1. **The Parking Lot Test**: Read the first two pages. Does this sound like two friends talking?
   Or does it sound like a script? If it reads like a script, loosen it up — add interruptions,
   half-finished thoughts, "wait, I forgot to mention—" moments.

2. **The Temperature Check**: Track the emotional register through the script. Does it actually
   shift? Is there a clear difference between the comedy in Act 1 and the tension in Act 3?
   Or is it all one temperature?

3. **The Carmen Test**: Find Carmen's darkest moment in the script — where the story genuinely
   gets to her. Does her voice change? Does the comedy stop? That moment should feel sudden
   and real, not performed. It's the most powerful beat in every episode.

4. **The Specificity Test**: Find the scariest line. Is it scary because of specific, grounded
   details? Or because of dramatic adjectives? "The radio was tuned to static" beats "the
   terrifying scene" every time.

5. **The Speechify Test**: Remember that Speechify will flesh this out further. The script
   should be detailed enough to establish structure and character voice, but it doesn't need
   to be a final shooting script. Leave room for Speechify to breathe.

### Step 5: Output

Save the script to the repository's `scripts/` directory (create if needed):
```
dead-in-the-region-editor/scripts/ep##-title-slug.md
```

Also save to the outputs folder so the user can access it:
```
/sessions/practical-eager-knuth/mnt/outputs/ep##-title-slug-script.md
```

The script file should include a brief header with metadata:
```markdown
# Dead in the Region — Episode [N]: "[Title]"
# Script for Speechify Studio
# Speakers: [N] ([names])
# Target length: [X] minutes
# NOTE: Upload speaker profiles and audience data to Speechify separately.
# This script goes into the "Text Idea" field.

---

[Script begins here]
```

---

## Episode-Specific Notes

Some episodes require special handling:

### Episode 1 (Pilot)
Everything is being established. Prioritize chemistry over case complexity. Work in how the hosts
know each other naturally — "when you first moved here," "back when we were at IU." Don't
over-explain. The case (The Borman Lights) should be engaging but the hosts are the real hook.

### Episodes 4-5 (The Whiting Recordings, Parts 1-2)
First multi-episode arc. Carmen's tonal shift from comedian to genuinely scared storyteller needs
to feel earned. In Part 1, the humor drains out gradually. Part 2 picks up where Part 1's
cliffhanger left off — the foundry connection is now impossible to ignore.

### Episode 6 (Belle Gunness — first Dr. Vasquez episode)
Three-speaker dynamic. Vasquez brings academic depth without dryness. She and Nate have collegial
rapport. She finds Carmen hilarious in a way she tries to hide. Write their three-way dynamic
as a triangle, not two separate conversations.

### Episode 8 (Tape 7 — format-breaker)
Completely different structure. Nate and Carmen only bookend (3-4 minutes each end). The middle
is them READING and DESCRIBING a tape transcript, with Dr. Vasquez providing historical context.
No humor. No banter in the middle section. Pure atmospheric horror through description. The
script should feel like a different show.

### Episodes 9-11 (The Meridian Line trilogy)
Escalating three-part arc. Episode 9 connects threads. Episode 10 brings Vasquez back as they
close in. Episode 11 is the climax — sustained dread, emotional intensity, the foundry mystery
reaching its peak. The humor-to-horror ratio shifts dramatically across the three episodes.

### Episode 12 (Season Finale)
Warmer, more reflective. The hosts are processing the season. Vasquez appears for final context.
Foundry resolution (or deliberate non-resolution). The script should feel like an exhale after
Episode 11's intensity, but with enough unresolved threads to set up a potential Season 2.

---

## Companion Data (Do NOT Bake Into Script)

The following data stays separate and gets uploaded to Speechify's configuration fields directly.
The script skill reads these for reference but does NOT include them in the script output:

- **Speaker Profiles** (`data/speakers.json`) → Speechify Step 3 (Speaker Configuration)
- **Audience & Mood** (`data/audience.json`) → Speechify Step 2 (Audience & Mood)

See `references/speechify-workflow.md` for the complete field mapping and upload process.
