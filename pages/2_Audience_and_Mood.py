import streamlit as st
import json
import os

st.set_page_config(
    page_title="Dead in the Region — Audience & Mood",
    page_icon="👥",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Data helpers (inline to avoid import issues on Streamlit Cloud)
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _get_github_repo():
    try:
        from github import Github
        token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]
        g = Github(token)
        return g.get_repo(repo_name)
    except Exception:
        return None


def load_audience():
    path = os.path.join(DATA_DIR, "audience.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"audience": {}}


def save_audience(data):
    path = os.path.join(DATA_DIR, "audience.json")
    content = json.dumps(data, indent=2)
    with open(path, "w") as f:
        f.write(content)
    repo = _get_github_repo()
    if repo is None:
        return False, "GitHub not configured."
    try:
        try:
            existing = repo.get_contents("data/audience.json")
            repo.update_file("data/audience.json", "Update audience & mood settings", content, existing.sha)
        except Exception:
            repo.create_file("data/audience.json", "Update audience & mood settings", content)
        return True, "Committed to GitHub."
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
if "audience_data" not in st.session_state:
    st.session_state.audience_data = load_audience()

data = st.session_state.audience_data
aud = data.get("audience", {})

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔪 Dead in the Region")
    st.markdown("##### Audience & Mood Settings")
    st.divider()
    st.caption(
        "These templates are pasted into Speechify Studio's "
        "**Audience & Mood** fields (Step 2) for every episode. "
        "They stay the same across the season unless an episode "
        "needs a special override (format-breakers, finales)."
    )
    st.divider()
    st.markdown("**Speechify Step 2 Fields:**")
    st.markdown(
        "1. Primary Audience\n"
        "2. Geography & Background\n"
        "3. Values & Interests\n"
        "4. Mood\n"
        "5. Tone"
    )

# ---------------------------------------------------------------------------
# Main area — audience & mood editor
# ---------------------------------------------------------------------------
st.markdown("# 👥 Audience & Mood")
st.markdown("*These reusable templates are pasted into Speechify Step 2 for every episode.*")
st.divider()

# ── Primary Audience ──
st.markdown("### Primary Audience")
st.caption("Who is listening to this podcast?")
new_audience = st.text_area(
    "Primary Audience",
    value=aud.get("primary_audience", ""),
    height=120,
    key="aud_primary",
    label_visibility="collapsed",
)

st.divider()

# ── Geography & Background ──
st.markdown("### Geography & Background")
st.caption("Where are the listeners and what's their cultural context?")
new_geo = st.text_area(
    "Geography & Background",
    value=aud.get("geography_background", ""),
    height=120,
    key="aud_geo",
    label_visibility="collapsed",
)

st.divider()

# ── Values & Interests ──
st.markdown("### Values & Interests")
st.caption("What do the listeners care about?")
new_values = st.text_area(
    "Values & Interests",
    value=aud.get("values_interests", ""),
    height=150,
    key="aud_values",
    label_visibility="collapsed",
)

st.divider()

# ── Mood ──
st.markdown("### Mood")
st.caption("The overall atmospheric feeling of the podcast.")
new_mood = st.text_area(
    "Mood",
    value=aud.get("mood", ""),
    height=120,
    key="aud_mood",
    label_visibility="collapsed",
)

st.divider()

# ── Tone ──
st.markdown("### Tone")
st.caption("How the hosts and content sound — the delivery style.")
new_tone = st.text_area(
    "Tone",
    value=aud.get("tone", ""),
    height=120,
    key="aud_tone",
    label_visibility="collapsed",
)

st.divider()

# ── Save ──
col_save, col_status = st.columns([1, 3])

with col_save:
    save_clicked = st.button("💾 Save Audience & Mood", type="primary", use_container_width=True)

if save_clicked:
    data["audience"] = {
        "primary_audience": new_audience,
        "geography_background": new_geo,
        "values_interests": new_values,
        "mood": new_mood,
        "tone": new_tone,
    }
    st.session_state.audience_data = data

    gh_ok, gh_msg = save_audience(data)

    with col_status:
        if gh_ok:
            st.success(f"✅ Audience & Mood saved & committed! {gh_msg}")
        else:
            st.info(f"💾 Saved locally. {gh_msg}")

# ── Preview for copy-paste ──
st.divider()
st.markdown("### 📋 Quick Copy Reference")
st.caption("Expand to see the exact text to paste into each Speechify Step 2 field.")

with st.expander("Speechify Step 2 fields — full text", expanded=False):
    st.markdown("**Primary Audience:**")
    st.code(new_audience, language=None)
    st.markdown("**Geography & Background:**")
    st.code(new_geo, language=None)
    st.markdown("**Values & Interests:**")
    st.code(new_values, language=None)
    st.markdown("**Mood:**")
    st.code(new_mood, language=None)
    st.markdown("**Tone:**")
    st.code(new_tone, language=None)
