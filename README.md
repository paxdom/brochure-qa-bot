
````markdown
# 📄 PaXdom Brochure QA Bot  
### A Neutral AI Tool to Decode Property Brochures & Documents

**PaXdom Brochure QA Bot** is an AI-powered tool by **PaXdom Realty** that allows homebuyers to extract clear, neutral, and factual information from property brochures, PDFs, or pasted listing text.

It provides **structured answers to user questions** while highlighting what is stated, what is missing, and what requires attention — all **without promoting the property or providing buying advice**.

---

## Why PaXdom Built This Tool

At PaXdom Realty, we noticed that:
- Brochures and PDFs often hide trade-offs or limitations
- Marketing language can be confusing
- Buyers frequently miss key information
- It’s difficult to extract answers quickly from long documents

The **Brochure QA Bot** allows buyers to:
- Ask precise questions about a property
- Get factual, neutral answers
- Identify missing or ambiguous details
- Make informed property decisions

---

## How It Works (V1)

1. **Input**
   - Upload PDF brochures or property documents  
   - Or paste raw listing/brochure text

2. **Ask a Question**
   - Examples: “What is the total area?” / “Any amenities?” / “Possession date?”

3. **Output**
   - Structured answer including:  
     1. Question Asked  
     2. Answer (based strictly on content)  
     3. Missing or Unclear Information  
     4. Relevant Notes / Observations  

**Key Principles**
- Neutral, factual, and unbiased  
- Missing information explicitly flagged  
- No marketing, promotion, or ranking

---

## What the App Does NOT Do

- ❌ Does not promote, rank, or recommend properties  
- ❌ Does not provide legal, financial, or investment advice  
- ❌ Does not scrape external links (V1 works on uploaded or pasted text only)

---

## Technology Stack

- **Frontend**: Streamlit  
- **AI Model**: OpenAI (`gpt-4o-mini`)  
- **Language**: Python 3.11  

Chosen for simplicity, reliability, and low operating cost.

---

## Running the App Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Set OpenAI API key

Create the file:

```
.streamlit/secrets.toml
```

Add:

```toml
OPENAI_API_KEY = "sk-xxxx"
```

### 3. Run the app

```bash
streamlit run streamlit_app.py
```

---

## Cost Notes

Approximate usage cost:

* ₹0.10 – ₹0.30 per analysis (depends on PDF/text length)

---

## Product Philosophy

PaXdom Realty built this tool on three principles:

1. **Clarity over persuasion**
2. **Transparency over marketing**
3. **Buyer trust over short-term sales**

It is a **standalone clarity tool**, designed to help buyers make confident property decisions.

---

## Try It & Learn More

Explore more PaXdom Realty tools and listings at:
**[paxdomrealty.com](https://paxdomrealty.com)**

---

## Disclaimer

This tool provides **informational analysis only**.
It does **not** constitute legal, financial, or investment advice.
Users should always verify details independently and consult professionals when needed.

---

## License

---