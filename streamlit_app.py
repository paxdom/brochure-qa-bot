import streamlit as st
from openai import OpenAI
import pdfplumber

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Brochure QA Bot",
    page_icon="📄",
    layout="centered"
)

# -------------------------------------------------
# GLOBAL UI FIX (NO SCROLL / NO THEME ISSUES)
# -------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Typography */
h1, h2, h3 {
    color: #111827 !important;
}

/* Inputs */
textarea, input {
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Buttons */
button {
    background-color: #111827 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Remove internal scrollbars */
.main, .block-container {
    overflow: visible !important;
    max-height: none !important;
}

/* Markdown */
.stMarkdown {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:30px;">
    <h1 style="margin-bottom:10px;">📄 Brochure QA Bot</h1>
    <p style="
        color:#374151;
        font-size:15px;
        max-width:680px;
        margin:auto;
        line-height:1.6;
    ">
        Upload property brochures, PDFs, or paste listing text.<br>
        Ask questions and receive <b>neutral, factual answers</b> — including what is missing or unclear.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------
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
        st.success(f"Extracted content from {uploaded_file.name}")
    except Exception:
        st.error("Unable to read PDF file.")

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

# -------------------------------------------------
# CTA
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button(
    "🔍 Analyze Brochure",
    use_container_width=True
)

# -------------------------------------------------
# SYSTEM PROMPT (FINAL)
# -------------------------------------------------
SYSTEM_PROMPT = """
You are a neutral real estate analyst specializing in property brochures and listings.

Your task:
Answer the user's question using ONLY the information explicitly present in the provided brochure or listing text.

Strict rules:
- Do NOT assume, infer, recommend, or advise.
- Do NOT use general real estate knowledge.
- If something is not clearly stated, treat it as missing.
- Use short, neutral, factual language.
- Never promote or market the property.
- Never provide financial, legal, or personal advice.

If the question asks for opinions, decisions, or judgments (e.g., “Should I buy?”),
state clearly that the brochure does not provide decision guidance.

Output format (STRICT):

1. Question Asked
   [Repeat the user question exactly]

2. Answer (based strictly on brochure content)
   [Facts only. If not mentioned, say: "Not mentioned in the brochure."]

3. Missing or Unclear Information
   [List missing or ambiguous items relevant to the question. If none, write "None."]

4. Relevant Notes / Observations
   [Neutral observations directly derived from the text. No interpretation.]
"""

# -------------------------------------------------
# OUTPUT
# -------------------------------------------------
if analyze_clicked:
    if not brochure_content.strip() or not question.strip():
        st.warning("Please provide brochure text (or upload a PDF) and ask a question.")
    else:
        with st.spinner("Analyzing brochure objectively…"):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            user_prompt = f"""
Brochure Content:
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

        st.markdown("---")
        st.markdown("## 📊 Answer")

        st.markdown(
            f"""
            <div style="
                background:#F9FAFB;
                color:#111827;
                border:1px solid #E5E7EB;
                border-radius:10px;
                padding:22px;
                font-size:15px;
                line-height:1.7;
                white-space:pre-wrap;
            ">
{response.choices[0].message.content}
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Neutral analysis tool • Built for clarity, not persuasion")
