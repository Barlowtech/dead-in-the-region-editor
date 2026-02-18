import streamlit as st
import pandas as pd
import os
import io
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dead in the Region — Production Hub",
    page_icon="🔪",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "episodes.csv")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

# Structured field options
TYPE_OPTIONS = [
    "Real",
    "Fictional",
    "Fictional (presented ambiguously)",
    "Mixed (real framework + fictional case)",
    "Mixed (real case recontextualized)",
    "Mixed",
]
FORMAT_OPTIONS = [
    "Standalone",
    "Standalone (with guest)",
    "Part 1 of 2",
    "Part 2 of 2",
    "Part 1 of 3",
    "Part 2 of 3",
    "Part 3 of 3",
    "Found audio / recovered recording",
    "Season wrap / reflection / tease",
]
TOLD_BY_OPTIONS = ["Nate", "Carmen", "Both", "Neither (format-breaker)"]
SPEAKER_OPTIONS = ["2", "3"]
GUEST_OPTIONS = ["None", "Dr. Mara Vasquez", "Dr. Mara Vasquez (interstitials only)"]

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    """Load CSV, filling NaN with empty strings."""
    df = pd.read_csv(path, dtype=str).fillna("")
    return df


def save_csv_local(df: pd.DataFrame, path: str):
    """Write dataframe back to the local CSV file."""
    df.to_csv(path, index=False)


def commit_to_github(df: pd.DataFrame):
    """Push updated CSV to the GitHub repo (if secrets are configured)."""
    try:
        from github import Github

        token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]       # e.g. "user/repo"
        file_path = st.secrets["github"].get("file_path", "data/episodes.csv")
        branch = st.secrets["github"].get("branch", "main")

        g = Github(token)
        repo = g.get_repo(repo_name)
        contents = repo.get_contents(file_path, ref=branch)

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        new_content = csv_buffer.getvalue()

        repo.update_file(
            path=file_path,
            message=f"Update episodes.csv — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            content=new_content,
            sha=contents.sha,
            branch=branch,
        )
        return True, "Changes committed to GitHub."
    except ImportError:
        return False, "PyGithub not installed — saved locally only."
    except KeyError:
        return False, "GitHub secrets not configured — saved locally only."
    except Exception as e:
        return False, f"GitHub push failed: {e}"


def commit_prompt_to_github(filename: str, content: str):
    """Push a single prompt file to the GitHub repo."""
    try:
        from github import Github

        token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]
        branch = st.secrets["github"].get("branch", "main")

        g = Github(token)
        repo = g.get_repo(repo_name)
        file_path = f"prompts/{filename}"

        try:
            existing = repo.get_contents(file_path, ref=branch)
            repo.update_file(
                path=file_path,
                message=f"Update prompt: {filename} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=content,
                sha=existing.sha,
                branch=branch,
            )
        except Exception:
            repo.create_file(
                path=file_path,
                message=f"Add prompt: {filename} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=content,
                branch=branch,
            )
        return True, f"Prompt committed to GitHub: prompts/{filename}"
    except ImportError:
        return False, "PyGithub not installed — saved locally only."
    except KeyError:
        return False, "GitHub secrets not configured — saved locally only."
    except Exception as e:
        return False, f"GitHub push failed: {e}"


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert a title to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def generate_prompt_text(row: pd.Series) -> str:
    """Generate a Speechify-ready prompt from a CSV row."""
    ep_num = row.get("Episode", "")
    title = row.get("Title", "")
    ep_type = row.get("Type", "")
    fmt = row.get("Format", "")
    told_by = row.get("Told By", "")
    speakers = row.get("Speakers", "2")
    guest = row.get("Guest", "None")
    synopsis = row.get("Synopsis", "")
    case_hook = row.get("Case Hook", "")
    cold_open = row.get("Cold Open Concept", "")
    source_attr = row.get("Story Source Attribution", "")
    dynamic_story = row.get("Host Dynamic - Story Related", "")
    dynamic_personal = row.get("Host Dynamic - Personal Moments", "")
    humor = row.get("Humor Beats", "")
    horror = row.get("Horror Beats", "")
    foundry = row.get("Foundry Connection", "")
    arc_role = row.get("Season Arc Role", "")
    callbacks = row.get("Callbacks to Previous Episodes", "")
    tease = row.get("Next Episode Tease", "")
    tone_arc = row.get("Tone Arc", "")
    notes = row.get("Special Production Notes", "")

    # Build the hosts line
    hosts_line = "Nate Alderman (narrator/researcher) and Carmen Reyes (reactor/comedian)"
    if guest and guest != "None":
        hosts_line += f" + {guest}"

    # Build the host dynamics section
    dynamics_parts = []
    if told_by:
        dynamics_parts.append(f"PRIMARY STORYTELLER: {told_by}")
    if dynamic_story:
        dynamics_parts.append(f"\n{dynamic_story}")
    if dynamic_personal:
        dynamics_parts.append(f"\nPERSONAL MOMENTS (non-case interactions):\n{dynamic_personal}")
    if source_attr:
        dynamics_parts.append(f"\nSOURCE ATTRIBUTION:\n{source_attr}")
    host_dynamics_block = "\n".join(dynamics_parts)

    # Build serialization notes
    serial_parts = []
    if foundry:
        serial_parts.append(f"FOUNDRY CONNECTION: {foundry}")
    if arc_role:
        serial_parts.append(f"SEASON ARC ROLE: {arc_role}")
    if callbacks:
        serial_parts.append(f"CALLBACKS: {callbacks}")
    serialization_block = "\n\n".join(serial_parts)

    # Assemble the full prompt
    prompt = f"""PODCAST: Dead in the Region — Episode {ep_num}: "{title}"
FORMAT: {fmt}
TYPE: {ep_type}
HOSTS: {hosts_line}
SPEAKERS: {speakers}

---

COLD OPEN (0:00–0:45):
{cold_open}

---

THE CASE:
[Type: {ep_type}]

{synopsis}

CASE HOOK (the single most compelling detail):
{case_hook}

---

HOST DYNAMICS FOR THIS EPISODE:
{host_dynamics_block}

---

TONAL MAP:
{tone_arc}

---

HORROR/ATMOSPHERE BEATS:
{horror}

---

DARK HUMOR BEATS:
{humor}

---

SERIALIZATION NOTES:
{serialization_block}

---

NEXT EPISODE TEASE:
{tease}

---

PRODUCTION NOTES:
{notes}"""

    return prompt


def generate_prompt_filename(row: pd.Series) -> str:
    """Generate a consistent filename for a prompt file."""
    ep_num = str(row.get("Episode", "0")).zfill(2)
    title = row.get("Title", "untitled")
    return f"ep{ep_num}-{slugify(title)}.md"


def save_prompt_local(filename: str, content: str):
    """Save a prompt file to the local prompts/ directory."""
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Load data into session state
# ---------------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = load_csv(DATA_PATH)

if "selected_ep" not in st.session_state:
    st.session_state.selected_ep = 0  # index into dataframe

df = st.session_state.df

# ---------------------------------------------------------------------------
# Sidebar — episode selector + actions
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔪 Dead in the Region")
    st.markdown("##### Season 1 Episode Editor")
    st.divider()

    # Episode list
    for idx, row in df.iterrows():
        ep_num = row.get("Episode", idx + 1)
        title = row.get("Title", f"Episode {ep_num}")
        told_by = row.get("Told By", "")
        ep_type = row.get("Type", "")

        # Visual indicator for type
        type_icon = {"Real": "📰", "Fictional": "👻", "Mixed": "🔀"}.get(
            ep_type.split("(")[0].strip().split(" ")[0], "📝"
        )

        label = f"**Ep {ep_num}** {type_icon} {title}"
        if st.button(
            f"Ep {ep_num}: {title}",
            key=f"ep_btn_{idx}",
            use_container_width=True,
            type="primary" if st.session_state.selected_ep == idx else "secondary",
        ):
            st.session_state.selected_ep = idx
            st.rerun()

    st.divider()

    # ── Prompt generation (all episodes) ──
    if st.button("⚡ Generate All Prompts", use_container_width=True):
        results = []
        for i, r in df.iterrows():
            prompt_text = generate_prompt_text(r)
            fname = generate_prompt_filename(r)
            save_prompt_local(fname, prompt_text)
            ok, msg = commit_prompt_to_github(fname, prompt_text)
            results.append((fname, ok, msg))

        successes = sum(1 for _, ok, _ in results if ok)
        st.success(f"✅ Generated {successes}/{len(results)} prompts and committed to GitHub.")
        if successes < len(results):
            for fname, ok, msg in results:
                if not ok:
                    st.warning(f"⚠️ {fname}: {msg}")

    st.divider()

    # Export CSV download
    csv_export = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv_export,
        file_name="dead-in-the-region-episodes.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Main area — episode editor form
# ---------------------------------------------------------------------------
idx = st.session_state.selected_ep
row = df.iloc[idx]

ep_num = row.get("Episode", idx + 1)
title = row.get("Title", "")

st.markdown(f"# Episode {ep_num}: \"{title}\"")
st.divider()


def safe_index(options: list, value: str, default: int = 0) -> int:
    """Return index of value in options, or default if not found."""
    try:
        return options.index(value)
    except ValueError:
        # Try partial match
        for i, opt in enumerate(options):
            if value.strip().lower() in opt.lower() or opt.lower() in value.strip().lower():
                return i
        return default


# ── Structure ──────────────────────────────────────────────────────────────
st.markdown("### 📋 Structure")
col1, col2, col3, col4 = st.columns(4)

with col1:
    new_title = st.text_input("Title", value=title, key=f"title_{idx}")
with col2:
    new_type = st.selectbox(
        "Type",
        TYPE_OPTIONS,
        index=safe_index(TYPE_OPTIONS, row.get("Type", "")),
        key=f"type_{idx}",
    )
with col3:
    new_format = st.selectbox(
        "Format",
        FORMAT_OPTIONS,
        index=safe_index(FORMAT_OPTIONS, row.get("Format", "")),
        key=f"format_{idx}",
    )
with col4:
    new_told_by = st.selectbox(
        "Told By",
        TOLD_BY_OPTIONS,
        index=safe_index(TOLD_BY_OPTIONS, row.get("Told By", "")),
        key=f"told_{idx}",
    )

col5, col6 = st.columns(2)
with col5:
    new_speakers = st.selectbox(
        "Speakers",
        SPEAKER_OPTIONS,
        index=safe_index(SPEAKER_OPTIONS, str(row.get("Speakers", "2"))),
        key=f"speakers_{idx}",
    )
with col6:
    new_guest = st.selectbox(
        "Guest",
        GUEST_OPTIONS,
        index=safe_index(GUEST_OPTIONS, row.get("Guest", "None")),
        key=f"guest_{idx}",
    )

st.divider()

# ── Story ──────────────────────────────────────────────────────────────────
st.markdown("### 📖 Story")

new_synopsis = st.text_area(
    "Synopsis",
    value=row.get("Synopsis", ""),
    height=180,
    key=f"synopsis_{idx}",
)
new_case_hook = st.text_area(
    "Case Hook — the single most compelling detail",
    value=row.get("Case Hook", ""),
    height=100,
    key=f"hook_{idx}",
)
new_cold_open = st.text_area(
    "Cold Open Concept",
    value=row.get("Cold Open Concept", ""),
    height=120,
    key=f"cold_{idx}",
)
new_source = st.text_area(
    "Story Source Attribution — what Nate/Carmen claims as their source",
    value=row.get("Story Source Attribution", ""),
    height=120,
    key=f"source_{idx}",
)

st.divider()

# ── Host Dynamic ───────────────────────────────────────────────────────────
st.markdown("### 🎭 Host Dynamic")

new_dynamic_story = st.text_area(
    "Story-Related Dynamic — how they interact about the case",
    value=row.get("Host Dynamic - Story Related", ""),
    height=150,
    key=f"dynamic_story_{idx}",
)
new_dynamic_personal = st.text_area(
    "Personal Moments — interactions NOT about the case",
    value=row.get("Host Dynamic - Personal Moments", ""),
    height=150,
    key=f"dynamic_personal_{idx}",
)

col_h, col_hr = st.columns(2)
with col_h:
    new_humor = st.text_area(
        "Humor Beats",
        value=row.get("Humor Beats", ""),
        height=150,
        key=f"humor_{idx}",
    )
with col_hr:
    new_horror = st.text_area(
        "Horror Beats",
        value=row.get("Horror Beats", ""),
        height=150,
        key=f"horror_{idx}",
    )

st.divider()

# ── Season Arc ─────────────────────────────────────────────────────────────
st.markdown("### 🔗 Season Arc")

col_a, col_b = st.columns(2)
with col_a:
    new_foundry = st.text_area(
        "Foundry Connection",
        value=row.get("Foundry Connection", ""),
        height=120,
        key=f"foundry_{idx}",
    )
    new_callbacks = st.text_area(
        "Callbacks to Previous Episodes",
        value=row.get("Callbacks to Previous Episodes", ""),
        height=100,
        key=f"callbacks_{idx}",
    )
with col_b:
    new_arc_role = st.text_area(
        "Season Arc Role",
        value=row.get("Season Arc Role", ""),
        height=120,
        key=f"arc_{idx}",
    )
    new_tease = st.text_area(
        "Next Episode Tease",
        value=row.get("Next Episode Tease", ""),
        height=100,
        key=f"tease_{idx}",
    )

st.divider()

# ── Tone & Production ─────────────────────────────────────────────────────
st.markdown("### 🎨 Tone & Production")

new_tone = st.text_area(
    "Tone Arc — how the emotional register moves within the episode",
    value=row.get("Tone Arc", ""),
    height=100,
    key=f"tone_{idx}",
)
new_notes = st.text_area(
    "Special Production Notes — Speechify-specific guidance and creative priorities",
    value=row.get("Special Production Notes", ""),
    height=120,
    key=f"notes_{idx}",
)

st.divider()

# ── Save & Generate ───────────────────────────────────────────────────────
col_save, col_gen, col_status = st.columns([1, 1, 2])

with col_save:
    save_clicked = st.button("💾 Save Episode", type="primary", use_container_width=True)

with col_gen:
    gen_clicked = st.button("⚡ Generate Prompt", use_container_width=True)

if save_clicked:
    # Update the dataframe
    updates = {
        "Title": new_title,
        "Type": new_type,
        "Format": new_format,
        "Told By": new_told_by,
        "Speakers": new_speakers,
        "Guest": new_guest,
        "Synopsis": new_synopsis,
        "Case Hook": new_case_hook,
        "Cold Open Concept": new_cold_open,
        "Story Source Attribution": new_source,
        "Host Dynamic - Story Related": new_dynamic_story,
        "Host Dynamic - Personal Moments": new_dynamic_personal,
        "Humor Beats": new_humor,
        "Horror Beats": new_horror,
        "Foundry Connection": new_foundry,
        "Season Arc Role": new_arc_role,
        "Callbacks to Previous Episodes": new_callbacks,
        "Next Episode Tease": new_tease,
        "Tone Arc": new_tone,
        "Special Production Notes": new_notes,
    }

    for col, val in updates.items():
        if col in df.columns:
            df.at[idx, col] = val

    st.session_state.df = df

    # Save locally
    save_csv_local(df, DATA_PATH)

    # Try GitHub commit
    gh_success, gh_msg = commit_to_github(df)

    with col_status:
        if gh_success:
            st.success(f"✅ Saved & committed! {gh_msg}")
        else:
            st.info(f"💾 Saved locally. {gh_msg}")

    # Clear the cached data so next load picks up changes
    load_csv.clear()

if gen_clicked:
    # Generate prompt from current row data (uses saved data, not form state)
    prompt_text = generate_prompt_text(row)
    fname = generate_prompt_filename(row)

    # Save locally
    save_prompt_local(fname, prompt_text)

    # Commit to GitHub
    gh_ok, gh_msg = commit_prompt_to_github(fname, prompt_text)

    with col_status:
        if gh_ok:
            st.success(f"⚡ Prompt generated & committed! `prompts/{fname}`")
        else:
            st.info(f"⚡ Prompt saved locally. {gh_msg}")

    # Show the generated prompt in an expander
    with st.expander(f"📄 Generated Prompt — {fname}", expanded=True):
        st.code(prompt_text, language="markdown")
