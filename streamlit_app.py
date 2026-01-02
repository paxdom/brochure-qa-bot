import streamlit as st
from openai import OpenAI
import pdfplumber

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="PaXdom Brochure QA Bot",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:20px;">
        <h1 style="margin-bottom:6px;">📄 Brochure QA Bot</h1>
        <p style="color:#555; font-size:15px; max-width:700px; margin:auto;">
            Upload property brochures, PDFs, or paste listing text, then ask questions.
            Receive clear, neutral, and factual answers highlighting what is missing or unclear.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# INPUT SECTION
# -----------------------------
st.markdown("### 🧾 Provide Brochure or Listing Details")

# PDF Upload
uploaded_file = st.file_uploader(
    "Upload PDF brochure or property document (optional)",
    type=["pdf"],
    help="PDFs can be property brochures, project brochures, or other official documents."
)

pdf_text = ""
if uploaded_file:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.success(f"Extracted {len(pdf_text.split())} words from {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")

# Text Area Input
text_input = st.text_area(
    "Or paste brochure/listing text here",
    placeholder=(
        "Paste WhatsApp messages, website listings, or brochure content.\n"
        "Tip: The more complete the text, the more accurate the analysis."
    ),
    height=220,
    key="brochure_text_input"
)

# Merge inputs
brochure_content = "\n".join(filter(None, [pdf_text, text_input]))

# Question Input
question = st.text_input(
    "Ask a specific question about the property",
    placeholder="Example: What is the total area? Any amenities? Possession date?",
    key="brochure_question"
)

# -----------------------------
# CTA BUTTON
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button(
    "🔍 Analyze Brochure",
    use_container_width=True
)

# -----------------------------
# SYSTEM PROMPT (REFINED)
# -----------------------------
SYSTEM_PROMPT = """
You are a neutral real estate analyst specialized in property brochures and listings.

Your task:
Answer user questions strictly based on the content provided (PDF text or pasted listing). 
Do NOT assume or infer any information not explicitly present in the text. 
Do NOT provide advice, opinions, or recommendations.

Rules:
- Use only the information in the brochure or listing. 
- Highlight missing, unclear, or ambiguous information clearly. 
- Use short, simple, neutral, and factual language. 
- Never promote, market, or sell the property.
- Never provide financial, legal, or personal advice.
- If a question cannot be answered based on the text, explicitly state "Not mentioned in the brochure."
- Maintain the following output structure exactly, even if some sections are empty:

Output format:

1. Question Asked  
   [Repeat the user’s question exactly]

2. Answer (based strictly on brochure content)  
   [Provide only facts present in the text. Do NOT add assumptions or advice.]

3. Missing or Unclear Information  
   [List anything not mentioned, ambiguous, or unclear in the brochure that is relevant to the question. If everything is mentioned, write "None."]

4. Relevant Notes / Observations  
   [Any neutral observations strictly derived from the text. Do NOT interpret or suggest action.]
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

        st.markdown("---")
        st.markdown("## 📊 Answer")
        st.markdown(
            f"""
            <div style="
                background:#FAFAFA;
                border:1px solid #E5E7EB;
                border-radius:8px;
                padding:20px;
                line-height:1.6;
                font-size:15px;
                word-wrap:break-word;
            ">
            {response.choices[0].message.content}
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("PaXdom AI Tools • Neutral analysis • Built for informed decisions")
