import streamlit as st
from utils import get_explanation

# ── Page configuration ──
st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="centered"
)

# ── Header ──
st.title("📚 Student Study Buddy")
st.caption("Paste any topic or study note. Get an explanation, summary, and practice questions instantly.")
st.divider()

# ── Subject selector ──
subject = st.selectbox(
    "Select your subject (optional):",
    ["General", "Computer Science", "Mathematics",
     "Machine Learning", "Networks & Security", "GATE Prep"]
)

# ── Input ──
topic = st.text_area(
    "Enter a topic or paste your study notes:",
    placeholder="e.g. LL(1) parsing, Dijkstra's algorithm, Bayes theorem ...",
    height=150
)

# ── Button ──
if st.button("Explain this topic", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Thinking... (usually takes 3-5 seconds)"):
            result = get_explanation(topic)

        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state["last_result"] = result
            st.session_state["last_topic"]  = topic

# ── Display result ──
if "last_result" in st.session_state:
    st.divider()
    sections = st.session_state["last_result"].split("##")
    for section in sections:
        if section.strip():
            lines   = section.strip().split("\n", 1)
            heading = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            with st.expander(heading, expanded=True):
                st.markdown(content)

    st.divider()
    st.info("PDF download coming soon.")

# ── Footer ──
st.divider()
st.caption("Built with Python, Groq LLaMA 3, and Streamlit · ₹0 cost · Open source")