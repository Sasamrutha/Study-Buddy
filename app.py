import streamlit as st
from utils import get_explanation
from pdf_utils import generate_pdf

# ── Page configuration ──
st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="centered"
)

# ── Custom CSS ──
st.markdown("""
<style>
    .stApp { background-color: #FAFAF8; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1A1916; margin-bottom: 0px; }
    .sub-title { font-size: 1rem; color: #5C5A55; margin-bottom: 2rem; }
    .stButton > button { background-color: #E07B39; color: white; border: none; border-radius: 8px; padding: 0.6rem 1.2rem; font-size: 1rem; font-weight: 600; width: 100%; transition: background-color 0.2s; }
    .stButton > button:hover { background-color: #C5682A; color: white; }
    .section-card { background-color: #FFFFFF; border: 1px solid #E2DED6; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
    .section-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #E07B39; margin-bottom: 0.6rem; }
    .section-content { font-size: 0.95rem; color: #1A1916; line-height: 1.7; }
    .stTextArea textarea { border-radius: 8px; border: 1px solid #E2DED6; font-size: 0.95rem; }
    .stSelectbox > div > div { border-radius: 8px; border: 1px solid #E2DED6; }
    hr { border-color: #E2DED6; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 📚 Study Buddy")
    st.markdown("**How to use:**")
    st.markdown("1. Select your subject")
    st.markdown("2. Type any topic")
    st.markdown("3. Click Explain")
    st.markdown("4. Download PDF")
    st.divider()
    st.markdown("Built by [Sasamrutha](https://github.com/Sasamrutha)")
    st.markdown("⭐ Star on [GitHub](https://github.com/Sasamrutha/Study-Buddy)")

# ── Header ──
st.markdown('<div class="main-title">📚 Study Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Paste any topic. Get a plain-English explanation, summary, and practice questions instantly.</div>', unsafe_allow_html=True)
st.divider()

# ── Subject selector ──
subject = st.selectbox(
    "Subject",
    ["General", "Computer Science", "Mathematics",
     "Machine Learning", "Networks & Security", "GATE Prep"],
    label_visibility="collapsed"
)

# ── Input ──
topic = st.text_area(
    "Topic",
    placeholder="e.g. LL(1) parsing, Dijkstra's algorithm, Bayes theorem, RSA encryption ...",
    height=130,
    label_visibility="collapsed"
)
st.caption(f"{len(topic)}/500 characters")

# ── Buttons ──
col1, col2 = st.columns([4, 1])
with col1:
    explain = st.button("Explain this topic →", use_container_width=True)
with col2:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.session_state.pop("last_result", None)
    st.session_state.pop("last_topic", None)
    st.rerun()

if explain:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating explanation..."):
            result = get_explanation(topic)
        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state["last_result"] = result
            st.session_state["last_topic"]  = topic

# ── Display result ──
if "last_result" in st.session_state:
    st.divider()
    icons = {
        "SIMPLE EXPLANATION": "💡",
        "5-POINT SUMMARY": "📋",
        "PRACTICE QUESTIONS": "✏️",
        "DIFFICULTY RATING": "⭐"
    }
    sections = st.session_state["last_result"].split("##")
    for section in sections:
        if section.strip():
            lines   = section.strip().split("\n", 1)
            heading = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            icon    = icons.get(heading, "📌")
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">{icon} {heading}</div>
                <div class="section-content">{content.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    pdf_bytes = generate_pdf(
        st.session_state["last_topic"],
        st.session_state["last_result"]
    )
    st.download_button(
        label="📄 Download as PDF revision sheet",
        data=pdf_bytes,
        file_name="studybuddy_revision.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ── Footer ──
st.markdown("<br>", unsafe_allow_html=True)
st.caption("Built with Python · Groq LLaMA 3 · Streamlit")