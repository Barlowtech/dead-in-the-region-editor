import streamlit as st
import json
import os

st.set_page_config(
    page_title="Dead in the Region — Speaker Profiles",
    page_icon="🎙️",
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


def load_speakers():
    path = os.path.join(DATA_DIR, "speakers.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"speakers": []}


def save_speakers(data):
    path = os.path.join(DATA_DIR, "speakers.json")
    content = json.dumps(data, indent=2)
    with open(path, "w") as f:
        f.write(content)
    # Commit to GitHub
    repo = _get_github_repo()
    if repo is None:
        return False, "GitHub not configured."
    try:
        try:
            existing = repo.get_contents("data/speakers.json")
            repo.update_file("data/speakers.json", "Update speaker profiles", content, existing.sha)
        except Exception:
            repo.create_file("data/speakers.json", "Update speaker profiles", content)
        return True, "Committed to GitHub."
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
if "speakers_data" not in st.session_state:
    st.session_state.speakers_data = load_speakers()

data = st.session_state.speakers_data
speakers = data.get("speakers", [])

# ---------------------------------------------------------------------------
# Sidebar — speaker selector
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔪 Dead in the Region")
    st.markdown("##### Speaker Profiles")
    st.divider()

    if "selected_speaker" not in st.session_state:
        st.session_state.selected_speaker = 0

    for i, spk in enumerate(speakers):
        label = f"{spk['name']} — {spk['role']}"
        if st.button(
            label,
            key=f"spk_btn_{i}",
            use_container_width=True,
            type="primary" if st.session_state.selected_speaker == i else "secondary",
        ):
            st.session_state.selected_speaker = i
            st.rerun()

    st.divider()
    st.caption("These profiles are pasted into Speechify Studio's Speaker fields for every episode.")

# ---------------------------------------------------------------------------
# Main area — profile editor
# ---------------------------------------------------------------------------
if not speakers:
    st.warning("No speaker profiles found. Check data/speakers.json.")
    st.stop()

idx = st.session_state.selected_speaker
spk = speakers[idx]

st.markdown(f"# 🎙️ {spk['name']}")
st.markdown(f"**{spk['role']}** · {spk['type'].title()} · {spk['gender']}, {spk['age']}")
if spk.get("episodes"):
    st.markdown(f"**Appears in:** {spk['episodes']}")
st.divider()

# ── Identity ──
st.markdown("### Identity")
col1, col2, col3 = st.columns(3)

with col1:
    new_name = st.text_input("Name (as shown in Speechify)", value=spk["name"], key=f"spk_name_{idx}")
with col2:
    new_role = st.text_input("Role", value=spk["role"], key=f"spk_role_{idx}")
with col3:
    type_opts = ["host", "guest"]
    new_type = st.selectbox(
        "Type",
        type_opts,
        index=type_opts.index(spk.get("type", "host")) if spk.get("type", "host") in type_opts else 0,
        key=f"spk_type_{idx}",
    )

col4, col5, col6 = st.columns(3)
with col4:
    new_gender = st.text_input("Gender", value=spk.get("gender", ""), key=f"spk_gender_{idx}")
with col5:
    new_age = st.text_input("Age", value=spk.get("age", ""), key=f"spk_age_{idx}")
with col6:
    new_episodes = st.text_input("Episodes", value=spk.get("episodes", "All"), key=f"spk_eps_{idx}")

st.divider()

# ── Biography (Speechify field) ──
st.markdown("### Biography")
st.caption("This text is pasted directly into Speechify's **Biography** field for this speaker.")
new_bio = st.text_area(
    "Biography",
    value=spk.get("biography", ""),
    height=250,
    key=f"spk_bio_{idx}",
    label_visibility="collapsed",
)

bio_words = len(new_bio.split()) if new_bio.strip() else 0
st.caption(f"{bio_words} words")

st.divider()

# ── Voice Style (Speechify field) ──
st.markdown("### Voice Style")
st.caption("This text is pasted directly into Speechify's **Voice Style** field for this speaker.")
new_voice = st.text_area(
    "Voice Style",
    value=spk.get("voice_style", ""),
    height=250,
    key=f"spk_voice_{idx}",
    label_visibility="collapsed",
)

voice_words = len(new_voice.split()) if new_voice.strip() else 0
st.caption(f"{voice_words} words")

st.divider()

# ── Save ──
col_save, col_status = st.columns([1, 3])

with col_save:
    save_clicked = st.button("💾 Save Profile", type="primary", use_container_width=True)

if save_clicked:
    speakers[idx] = {
        "id": spk.get("id", new_name.lower().split()[0] if new_name else "unknown"),
        "name": new_name,
        "role": new_role,
        "type": new_type,
        "gender": new_gender,
        "age": new_age,
        "episodes": new_episodes,
        "biography": new_bio,
        "voice_style": new_voice,
    }
    data["speakers"] = speakers
    st.session_state.speakers_data = data

    gh_ok, gh_msg = save_speakers(data)

    with col_status:
        if gh_ok:
            st.success(f"✅ Profile saved & committed! {gh_msg}")
        else:
            st.info(f"💾 Saved locally. {gh_msg}")

# ── Preview for copy-paste ──
st.divider()
st.markdown("### 📋 Quick Copy Reference")
st.caption("Expand to see the exact text to paste into each Speechify field.")

with st.expander(f"Speechify fields for {spk['name']}", expanded=False):
    st.markdown("**Name Field:**")
    st.code(new_name, language=None)
    st.markdown("**Biography Field:**")
    st.code(new_bio, language=None)
    st.markdown("**Voice Style Field:**")
    st.code(new_voice, language=None)
