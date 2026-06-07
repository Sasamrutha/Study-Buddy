import streamlit as st
from utils import get_explanation
from pdf_utils import generate_pdf

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #533483 100%);
    min-height: 100vh;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Glass card ── */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-emoji {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    display: block;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
    margin-bottom: 0.75rem;
}
.hero-title .grad {
    background: linear-gradient(90deg, #A78BFA, #F59E0B, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    max-width: 420px;
    margin: 0 auto 1.5rem;
    line-height: 1.6;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 0.8rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Feature pills ── */
.feature-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.feature-pill {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 0.78rem;
    font-weight: 500;
    color: rgba(255,255,255,0.8);
}

/* ── Input label ── */
.input-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 14px !important;
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
    background: rgba(255,255,255,0.08) !important;
}
.stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.35) !important;
}

/* ── Topic chips ── */
.chips-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
    margin-bottom: 4px;
}
.chip {
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 500;
    color: #C4B5FD;
    cursor: pointer;
    transition: all 0.15s;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
    font-size: 0.95rem !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    padding: 0.65rem 1.5rem !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.12) !important;
}

/* ── Result cards ── */
.result-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.result-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}
.tag-explain { background: rgba(99,102,241,0.2); color: #A5B4FC; border: 1px solid rgba(99,102,241,0.3); }
.tag-summary { background: rgba(16,185,129,0.2); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.3); }
.tag-questions { background: rgba(245,158,11,0.2); color: #FCD34D; border: 1px solid rgba(245,158,11,0.3); }
.tag-difficulty { background: rgba(236,72,153,0.2); color: #F9A8D4; border: 1px solid rgba(236,72,153,0.3); }

.result-body {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.88);
    line-height: 1.8;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #F59E0B, #EF4444) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(245,158,11,0.3) !important;
    padding: 0.65rem !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(245,158,11,0.4) !important;
}

/* ── Char count ── */
.char-count {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.35);
    text-align: right;
    margin-top: 4px;
}

/* ── Trending row ── */
.trending-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.35);
}
.footer a { color: rgba(255,255,255,0.5); text-decoration: none; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.1) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #A78BFA !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 📚 Study Buddy")
    st.markdown("**How to use:**")
    st.markdown("1. Select your subject")
    st.markdown("2. Type or click a topic")
    st.markdown("3. Click Generate")
    st.markdown("4. Download PDF")
    st.divider()
    st.markdown("Built by [Sasamrutha](https://github.com/Sasamrutha)")
   
# ── Hero ──
st.markdown("""
<div class="hero">
    <span class="hero-emoji">📚</span>
    <div class="hero-title">Learn Any Topic<br><span class="grad">in Seconds.</span></div>
    <div class="hero-sub">Get plain-English explanations, revision notes, practice questions, and a downloadable PDF — instantly.</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──
st.markdown("""
<div class="stats-row">
    <span class="stat-pill"> Plain English Explanations</span>
    <span class="stat-pill"> Revision Notes</span>
    <span class="stat-pill"> Practice Questions</span>
    <span class="stat-pill"> PDF Download</span>
</div>
""", unsafe_allow_html=True)

# ── Input glass card ──
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown('<div class="input-label">Select Subject</div>', unsafe_allow_html=True)
subject = st.selectbox(
    "Subject",
    [" General", " Computer Science", " Mathematics",
     " Machine Learning", " Networks & Security", " GATE Prep"],
    label_visibility="collapsed"
)

st.markdown('<div class="input-label" style="margin-top:1rem">Enter Your Topic</div>', unsafe_allow_html=True)

# Handle chip clicks
if "chip_topic" not in st.session_state:
    st.session_state["chip_topic"] = ""

topic = st.text_area(
    "Topic",
    value=st.session_state["chip_topic"],
    placeholder="e.g. Binary Search Tree, Bayes theorem, RSA encryption...",
    height=110,
    label_visibility="collapsed"
)
st.markdown(f'<div class="char-count">{len(topic)} / 500</div>', unsafe_allow_html=True)

# ── Trending topic chips ──
st.markdown('<div class="trending-label"> Trending Topics</div>', unsafe_allow_html=True)
chips = ["Dijkstra", "Bayes Theorem", "OS Scheduling", "CNN", "Binary Tree", "DBMS", "RSA", "DP"]
cols = st.columns(len(chips))
for i, chip in enumerate(chips):
    with cols[i]:
        if st.button(chip, key=f"chip_{i}", use_container_width=True, type="secondary"):
            st.session_state["chip_topic"] = chip
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Action buttons ──
st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    generate = st.button("✨ Generate Explanation", type="primary", use_container_width=True)
with col2:
    clear = st.button("↺", type="secondary", use_container_width=True, help="Clear")

# ── Logic ──
if clear:
    st.session_state.pop("last_result", None)
    st.session_state.pop("last_topic", None)
    st.session_state["chip_topic"] = ""
    st.rerun()

if generate:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating your study notes..."):
            result = get_explanation(topic)
        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state["last_result"] = result
            st.session_state["last_topic"]  = topic
            st.session_state["chip_topic"]  = ""

# ── Results ──
if "last_result" in st.session_state:
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.85rem;font-weight:600;color:rgba(255,255,255,0.5);
    text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem">
    📖 Results for: <span style="color:#A78BFA">{st.session_state['last_topic']}</span>
    </div>
    """, unsafe_allow_html=True)

    tag_map = {
        "SIMPLE EXPLANATION": ( "Explanation",  "tag-explain"),
        "5-POINT SUMMARY":    ( "Summary",       "tag-summary"),
        "PRACTICE QUESTIONS": ( "Practice",      "tag-questions"),
        "DIFFICULTY RATING":  ( "Difficulty",    "tag-difficulty"),
    }

    sections = st.session_state["last_result"].split("##")
    for section in sections:
        if not section.strip():
            continue
        lines   = section.strip().split("\n", 1)
        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        icon, label, tag_cls = tag_map.get(heading, ("📌", heading, "tag-explain"))

        st.markdown(f"""
        <div class="result-card">
            <div class="result-tag {tag_cls}">{icon} {label}</div>
            <div class="result-body">{content.replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    pdf_bytes = generate_pdf(
        st.session_state["last_topic"],
        st.session_state["last_result"]
    )
    st.download_button(
        label=" Download PDF Revision Sheet",
        data=pdf_bytes,
        file_name="studybuddy_revision.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ── Footer ──
st.markdown("""
<div class="footer">
    Built with Python · Groq LLaMA 3 · Streamlit · ₹0 cost<br>
    <a href="https://github.com/Sasamrutha/Study-Buddy">GitHub</a>
</div>
""", unsafe_allow_html=True)