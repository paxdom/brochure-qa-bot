import streamlit as st
from openai import OpenAI
import pdfplumber

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Brochure QA Bot",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# GLOBAL SAFE CSS (MOBILE + EMBED)
# -----------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #111827 !important;
}

h1, h2, h3 {
    color: #111827 !important;
}

/* Inputs */
textarea, input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
}

/* Placeholder visibility fix */
textarea::placeholder,
input::placeholder {
    color: #6B7280 !important;
    opacity: 1 !important;
}

/* Button */
button {
    background-color: #111827 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Remove scroll traps */
.main, .block-container {
    overflow: visible !important;
    max-height: none !important;
}

/* Markdown spacing */
.stMarkdown h1, .stMarkdown h2 {
    margin-top: 1.2em;
}
.stMarkdown ul {
    padding-left: 1.2em;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:20px;">
        <h1>📄 Brochure QA Bot</h1>
        <p style="color:#555; font-size:15px; max-width:720px; margin:auto;">
            Upload property brochures or paste listing text.
            Ask direct questions and get neutral, factual answers — including what is missing or unclear.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# INPUT SECTION
# -----------------------------
st.markdown("### 🧾 Provide Brochure or Listing Details")

uploaded_file = st.file_uploader(
    "Upload PDF brochure (optional)",
    type=["pdf"]
)

pdf_text = ""
if uploaded_file:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            pdf_text = "\n".join(
                page.extract_text()
                for page in pdf.pages
                if page.extract_text()
            )
        st.success(f"Extracted {len(pdf_text.split())} words from {uploaded_file.name}")
    except Exception:
        st.error("Unable to read this PDF file.")

text_input = st.text_area(
    "Or paste brochure / listing text",
    placeholder="Paste WhatsApp messages, website listings, or brochure content here.",
    height=220
)

brochure_content = "\n".join(filter(None, [pdf_text, text_input]))

question = st.text_input(
    "Ask a specific question about the property",
    placeholder="Example: What is the possession date? What amenities are mentioned?"
)

# -----------------------------
# CTA
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button(
    "🔍 Analyze Brochure",
    use_container_width=True
)

# -----------------------------
# SYSTEM PROMPT (FINAL)
# -----------------------------
SYSTEM_PROMPT = """
You are a neutral real estate analyst specialized in property brochures and listings.

Your task:
Answer the user's question strictly using ONLY the provided brochure or listing text.

Rules:
- Do NOT assume, infer, or guess any information.
- Do NOT give opinions, advice, or recommendations.
- Do NOT promote, market, or sell the property.
- If information is missing, explicitly say "Not mentioned in the brochure."
- Use short, factual, neutral language.
- Highlight unclear or missing details clearly.
- Maintain the structure exactly.

Output format:

1. Question Asked
2. Answer (based strictly on brochure content)
3. Missing or Unclear Information
4. Relevant Notes / Observations
"""

# -----------------------------
# OUTPUT SECTION
# -----------------------------
if analyze_clicked:
    if not brochure_content.strip() or not question.strip():
        st.warning("Please provide brochure text (or upload PDF) AND ask a question.")
    else:
        with st.spinner("Analyzing brochure…"):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            user_prompt = f"""
Brochure / Listing Content:
{brochure_content}

User Question:
{question}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )

        # ✅ OUTPUT (SAFE, MOBILE-FRIENDLY)
        st.markdown("---")
        st.markdown("## 📊 Answer")

        with st.container():
            st.write(response.choices[0].message.content)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Neutral analysis • Built for clarity • No recommendations")
