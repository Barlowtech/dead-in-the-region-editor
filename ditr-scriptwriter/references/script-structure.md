# Script Structure — Dead in the Region

## Standard Episode Template

This is the narrative backbone for a standard (standalone or multi-part) episode. Every episode
follows this flow, though the timing and emphasis shift based on the episode's role in the season.

The timestamps below are approximate targets for a 25-30 minute episode.

---

### COLD OPEN (0:00–0:45) — ~100-150 words

The hook. Drop the listener into the most compelling moment of the episode with zero context.
This is almost always dialogue — Carmen or Nate saying something that raises an immediate question
the listener needs answered.

**Template:**
```
CARMEN: [The most unsettling or intriguing line from the episode]
NATE: [A reaction that deepens the mystery]
CARMEN: [A line that locks the hook]
```

**Rules:**
- Maximum 4-6 lines of dialogue
- No exposition. No "welcome to the show." No context.
- The listener should think "wait, WHAT?" and need to keep listening
- Use the Cold Open Concept from the CSV as your starting point — it's already been crafted
  for this purpose

**Example (Episode 1):**
```
CARMEN: His car was still running. Door open. Radio on. And that's it. That's all there was.
NATE: That can't be all there was.
CARMEN: That's what I said.
```

---

### ACT 1: THE SETUP (~0:45–8:00) — ~1,000-1,500 words

Two jobs here: (1) let the audience fall in love with the hosts, and (2) set up the case.

**Scene 1A: Banter & Personal Moments** (~0:45–3:00)

The hosts ease into the episode. This is where the personal relationship lives — the stuff
from the "Host Dynamic - Personal Moments" field. They're not performing yet. They're just
two friends settling into a conversation.

```
NATE: [Something about his week, a callback to a previous episode, or a personal detail]
CARMEN: [A reaction, a joke, a rib about Nate being an outsider]
NATE: [Dry response]
CARMEN: [Laughs]
```

**What goes here:**
- How they know each other (subtle, not expository — "back when we were at IU")
- Running jokes from previous episodes (if applicable)
- Carmen's Merrillville job complaints (brief, she shuts it down fast)
- Nate's GPS/highway confusion (early episodes)
- Any personal dynamic from the "Host Dynamic - Personal Moments" CSV field

**Scene 1B: Case Introduction** (~3:00–8:00)

The storyteller starts setting up the case. This is where source attribution lives.

```
CARMEN: Okay so. I found something this week.
NATE: You always find something.
CARMEN: No, this is different. So there's this Reddit thread—
NATE: Oh no.
CARMEN: —from 2016, on r/UnresolvedMysteries, and it's about [location in NWI]...
```

**What goes here:**
- The storyteller's source (from "Story Source Attribution" field) — woven into dialogue
- The case setup: where, when, what the surface-level story is
- The other host's reactions (skepticism from Nate, excitement from Carmen)
- Geographic specificity — name the streets, the intersections, the landmarks
- The mood is still light here — humor is present

---

### ACT 2: THE CASE (~8:00–20:00) — ~2,000-2,500 words

The meat of the episode. The story unfolds in detail.

**Scene 2A: Building the Picture** (~8:00–13:00)

Details accumulate. The storyteller is in their element — Carmen with oral-tradition energy and
digressions, or Nate with cinematic pacing and primary sources. The other host is still reacting
with a mix of humor and genuine curiosity.

```
CARMEN: So the guy at the shop — my cousin's shop, not like a random shop—
NATE: Which shop?
CARMEN: Does it matter?
NATE: YES.
CARMEN: Fine, the one on Indianapolis Boulevard. Anyway, he says he was driving the Borman
that night and he saw—
```

**What goes here:**
- The bulk of the Synopsis content, broken into conversational storytelling
- Host Dynamic - Story Related interactions (disagreements, different interpretations)
- Humor Beats — placed naturally where the Tone Arc indicates comedy still lives
- Early horror details — the ones that are creepy but not yet devastating

**Scene 2B: The Shift** (~13:00–20:00)

This is where the temperature changes. The humor thins. Details get darker or stranger. The
non-storytelling host's reactions shift from jokes to genuine engagement or concern.

```
[Carmen's voice has changed. She's not performing anymore.]

CARMEN: (quieter) And then they found his car.
NATE: On the shoulder?
CARMEN: On the shoulder. Engine running. Door open. Radio on static. And no footprints.
NATE: What do you mean no footprints?
CARMEN: I mean the ground was soft — it had rained — and there were no footprints leading
away from the car. He just... wasn't there anymore.
```

**What goes here:**
- The Horror Beats from the CSV — translated into descriptive dialogue
- The Case Hook — the single most compelling detail, saved for maximum impact
- The Foundry Connection (if applicable) — as a detail in the story, not a separate callout
- Tonal shift happening in real time through the hosts' voices and reactions

---

### ACT 3: THE TURN (~20:00–27:00) — ~1,000-1,500 words

The most intense material. Comedy is gone. Both hosts are fully in the story.

**For standalone episodes:**
The case reaches its most disturbing or unresolved point. The hosts sit with the implications.
The silence between lines carries weight.

**For multi-part episodes:**
The cliffhanger lands. A connection is revealed. The episode cuts.

**For format-breakers (Episode 8):**
This is the tape content — hosts reading/describing the transcript.

```
NATE: (very quiet) I looked up the address. The house where they found the tapes.
CARMEN: Okay.
NATE: It's three blocks from the Meridian foundry.
CARMEN: Wait.
NATE: Yeah.
CARMEN: Nate.
NATE: I know.
```

**What goes here:**
- The episode's most unsettling revelation or moment
- Foundry/serialization reveals (if this is the episode for it)
- Minimal dialogue — let the weight of the information land
- Both hosts processing together, not performing

---

### OUTRO (~27:00–30:00) — ~400-600 words

The exhale. The hosts come back to being themselves.

```
[A beat of silence. Then:]

CARMEN: (exhaling) Okay.
NATE: Yeah.
CARMEN: So that happened.
NATE: [A small dry observation that breaks the tension just slightly]
CARMEN: [A laugh — smaller than usual, but real]
```

**What goes here:**
- Processing — the hosts talking through what they just discussed as real people
- A small tension-release joke (earned, not forced)
- Callbacks to Previous Episodes (from the CSV field) — natural, not expository
- Next Episode Tease (from the CSV field) — usually Nate's line
- Sign-off (brief, casual — "see you next week")

---

## Format-Breaker Template (Episode 8)

Episode 8 breaks the standard structure entirely:

```
COLD OPEN: Whispered voice (explorer) + Nate breaking in
BOOKEND INTRO (3-4 min): Nate and Carmen, subdued, introducing the tape
TAPE SECTIONS (20+ min): Hosts reading/describing the transcript
  - Interspersed with Dr. Vasquez historical context
  - No humor, no banter
  - Escalating dread through description
BOOKEND OUTRO (3-4 min): Nate and Carmen processing. Brief. Heavy.
```

---

## Multi-Part Episode Notes

**Part 1 of a multi-parter:**
- Standard structure through Acts 1-2
- Act 3 is a cliffhanger, not a resolution
- Next Episode Tease is replaced by the cliffhanger itself
- "Part two next week" or similar acknowledgment at the very end

**Part 2 (or 3) of a multi-parter:**
- Cold Open can be a brief callback to Part 1's cliffhanger
- Act 1 is shorter — less banter, more "picking up where we left off"
- The case information from Part 1 shouldn't be repeated wholesale — trust the listener

---

## Word Count Guide

| Section | Standalone | Multi-Part | Format-Breaker |
|---|---|---|---|
| Cold Open | 100-150 | 100-150 | 100-150 |
| Act 1 | 1,000-1,500 | 600-1,000 | N/A (bookend) |
| Act 2 | 2,000-2,500 | 2,000-2,500 | N/A (tape) |
| Act 3 | 1,000-1,500 | 800-1,200 | N/A (tape) |
| Outro | 400-600 | 200-400 | N/A (bookend) |
| **Total** | **4,500-6,250** | **3,700-5,250** | **4,000-5,500** |

These are targets, not hard limits. If a scene needs more room to breathe, let it breathe.
