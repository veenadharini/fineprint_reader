# app.py

import streamlit as st
import json
from fineprint_agent import analyze_fine_print
from stagehand_reader import get_fineprint_text

st.set_page_config(page_title="FinePrintReader", layout="centered")
st.title("🕵️ FinePrintReader")

# Initialize session state for extraction
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# --- Manual Paste Section ---
st.markdown("### ✍️ Paste Terms & Conditions")
st.text_area(
    "📋 Paste the fine print or policy text here",
    height=300,
    key="fineprint_input"
)

# --- Auto Extract Section ---
st.markdown("---")
st.markdown("### 🌐 Auto-Extract from Webpage")
url = st.text_input("Paste a webpage URL (e.g. https://temu.com)", key="url_input")

if st.button("🔎 Scan Webpage for Fine Print"):
    if not st.session_state.url_input.strip():
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Fetching page…"):
            try:
                st.session_state.extracted_text = get_fineprint_text(st.session_state.url_input)
                if st.session_state.extracted_text:
                    st.success("✅ Extracted fine print!")
                else:
                    st.error("❌ No paragraphs found on that page.")
            except Exception as e:
                st.error(f"Failed to extract from page: {e}")

# --- Display the text to be analyzed ---
st.markdown("---")
st.markdown("### 📄 Text to Analyze")
text_to_analyze = (
    st.session_state.extracted_text
    if st.session_state.extracted_text.strip()
    else st.session_state.fineprint_input
)
st.text_area("Extracted / Pasted Text", text_to_analyze, height=200, disabled=True)

# --- Analyze Section ---
st.markdown("---")
if st.button("🔍 Analyze Fine Print"):
    if not text_to_analyze.strip():
        st.warning("Please paste or extract text before analyzing.")
    else:
        with st.spinner("Analyzing…"):
            try:
                output = analyze_fine_print(text_to_analyze)
                st.markdown("#### 📤 Raw Response")
                st.code(output, language="json")

                # Extract and clean up JSON substring
                start = output.find("{")
                end = output.rfind("}") + 1
                snippet = output[start:end].replace("\n", "").replace("\r", "").replace("\\", "")

                # Auto-close if cut off
                if not snippet.strip().endswith("}"):
                    if snippet.strip().endswith(","):
                        snippet = snippet.rstrip(",")
                    if snippet.count("{") > snippet.count("}"):
                        snippet += "}"
                    if snippet.count("[") > snippet.count("]"):
                        snippet += "]}"

                try:
                    parsed = json.loads(snippet)
                    st.success("✅ Parsed Result")
                    st.json(parsed)
                    st.download_button(
                        "📥 Download JSON",
                        json.dumps(parsed, indent=2),
                        file_name="fineprint_analysis.json",
                        mime="application/json"
                    )
                except Exception:
                    st.warning("⚠️ Couldn't parse clean JSON. Best attempt below:")
                    st.code(snippet, language="json")

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
