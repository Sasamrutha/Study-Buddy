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
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Animated background orbs ── */
.bg-orb-1 {
    position: fixed;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    top: -100px;
    right: -100px;
    pointer-events: none;
    animation: float1 8s ease-in-out infinite;
}
.bg-orb-2 {
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
    bottom: -50px;
    left: -100px;
    pointer-events: none;
    animation: float2 10s ease-in-out infinite;
}
@keyframes float1 {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(30px) translateX(-20px); }
}
@keyframes float2 {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(-25px) translateX(15px); }
}

/* ── Glass card ── */
.glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    animation: fadeUp 0.5s ease-out;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    animation: fadeUp 0.4s ease-out;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}
.hero-title .grad {
    background: linear-gradient(90deg, #818CF8, #C084FC, #F472B6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.55);
    max-width: 400px;
    margin: 0 auto 1.5rem;
    line-height: 1.7;
}

/* ── Feature pills ── */
.pill-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.pill {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    color: rgba(255,255,255,0.65);
}

/* ── Input label ── */
.input-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
    margin-top: 1rem;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-size: 0.9rem !important;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.92) !important;
    border: 1.5px solid rgba(255,255,255,0.3) !important;
    border-radius: 14px !important;
    color: #1A1916 !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px !important;
    caret-color: #6366F1 !important;
}
.stTextArea textarea:focus {
    border-color: #818CF8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.2) !important;
    background: #FFFFFF !important;
}
.stTextArea textarea::placeholder {
    color: rgba(0,0,0,0.35) !important;
}
.stTextArea textarea::selection {
    background: rgba(99,102,241,0.3) !important;
    color: #1A1916 !important;
}

/* ── Char count ── */
.char-count {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
    text-align: right;
    margin-top: 5px;
    margin-bottom: 1rem;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.45) !important;
    padding: 0.65rem 1.5rem !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    box-shadow: 0 6px 28px rgba(99,102,241,0.6) !important;
    transform: translateY(-2px) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.07) !important;
    color: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.12) !important;
    transform: translateY(-1px) !important;
}

/* ── Result heading ── */
.result-heading {
    font-size: 0.78rem;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
    margin-top: 0.5rem;
}
.result-topic {
    color: #A5B4FC;
    font-weight: 700;
}

/* ── Result cards ── */
.result-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 12px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    animation: fadeUp 0.4s ease-out;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.result-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}
.tag-explain   { background: rgba(99,102,241,0.2);  color: #A5B4FC; border: 1px solid rgba(99,102,241,0.3);  }
.tag-summary   { background: rgba(16,185,129,0.2);  color: #6EE7B7; border: 1px solid rgba(16,185,129,0.3);  }
.tag-questions { background: rgba(245,158,11,0.2);  color: #FCD34D; border: 1px solid rgba(245,158,11,0.3);  }
.tag-difficulty{ background: rgba(236,72,153,0.2);  color: #F9A8D4; border: 1px solid rgba(236,72,153,0.3);  }

.result-body {
    font-size: 0.94rem;
    color: rgba(255,255,255,0.85);
    line-height: 1.85;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #F59E0B, #EF4444) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    width: 100% !important;
    padding: 0.65rem !important;
    box-shadow: 0 4px 20px rgba(245,158,11,0.35) !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(245,158,11,0.5) !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #818CF8 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.7) !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.25);
}
.footer a { color: rgba(255,255,255,0.4); text-decoration: none; }
.footer a:hover { color: #A5B4FC; }
</style>

<!-- Animated background orbs -->
<div class="bg-orb-1"></div>
<div class="bg-orb-2"></div>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Study Buddy**")
    st.markdown("Your AI-powered study companion.")
    st.divider()
    st.markdown("Designed by **Sasamrutha**")
    st.markdown("[GitHub](https://github.com/Sasamrutha) · [LinkedIn](https://linkedin.com/in/sasamrutha)")

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-title">
        Study smarter,<br>
        <span class="grad">not harder.</span>
    </div>
    <div class="hero-sub">
        Get plain-English explanations, revision notes,
        practice questions, and a downloadable PDF — instantly.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Feature pills ──
st.markdown("""
<div class="pill-row">
    <span class="pill">Plain English Explanations</span>
    <span class="pill">Revision Notes</span>
    <span class="pill">Practice Questions</span>
    <span class="pill">PDF Download</span>
</div>
""", unsafe_allow_html=True)

# ── Input glass card ──
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown('<div class="input-label">Select Subject</div>', unsafe_allow_html=True)
subject = st.selectbox(
    "Subject",
    ["General", "Computer Science", "Mathematics",
     "Machine Learning", "Networks & Security", "GATE Prep"],
    label_visibility="collapsed"
)

st.markdown('<div class="input-label">Enter Your Topic</div>', unsafe_allow_html=True)
topic = st.text_area(
    "Topic",
    placeholder="e.g. Binary Search Tree, Bayes theorem, RSA encryption, Dijkstra...",
    height=120,
    label_visibility="collapsed"
)
st.markdown(f'<div class="char-count">{len(topic)} / 500</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    generate = st.button("Generate Explanation", type="primary", use_container_width=True)
with col2:
    clear = st.button("Clear", type="secondary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Logic ──
if clear:
    st.session_state.pop("last_result", None)
    st.session_state.pop("last_topic", None)
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

# ── Results ──
if "last_result" in st.session_state:
    st.markdown("---")
    st.markdown(f"""
    <div class="result-heading">
        Results for: <span class="result-topic">{st.session_state['last_topic']}</span>
    </div>
    """, unsafe_allow_html=True)

    tag_map = {
        "SIMPLE EXPLANATION": ("Explanation",  "tag-explain"),
        "5-POINT SUMMARY":    ("Summary",       "tag-summary"),
        "PRACTICE QUESTIONS": ("Practice",      "tag-questions"),
        "DIFFICULTY RATING":  ("Difficulty",    "tag-difficulty"),
    }

    sections = st.session_state["last_result"].split("##")
    for section in sections:
        if not section.strip():
            continue
        lines   = section.strip().split("\n", 1)
        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        label, tag_cls = tag_map.get(heading, (heading, "tag-explain"))

        st.markdown(f"""
        <div class="result-card">
            <div class="result-tag {tag_cls}">{label}</div>
            <div class="result-body">{content.replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    pdf_bytes = generate_pdf(
        st.session_state["last_topic"],
        st.session_state["last_result"]
    )
    st.download_button(
        label="Download PDF Revision Sheet",
        data=pdf_bytes,
        file_name=f"{st.session_state['last_topic'][:40].replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ── Footer ──
st.markdown("""
<div class="footer">
    Built with Python · Groq LLaMA 3 · Streamlit 
</div>
""", unsafe_allow_html=True)