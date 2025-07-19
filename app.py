# app.py

import streamlit as st
import json
from fineprint_agent import analyze_fine_print

st.set_page_config(page_title="FinePrintFinder", layout="centered")
st.title("🕵️ FinePrintFinder")

fineprint_input = st.text_area(
    "📋 Paste the Terms & Conditions here",
    height=300,
    placeholder="e.g. By subscribing, you agree to automatic monthly payments..."
)

if st.button("🔍 Analyze"):
    if not fineprint_input.strip():
        st.warning("Please paste some text before analyzing.")
    else:
        with st.spinner("Analyzing…"):
            try:
                output = analyze_fine_print(fineprint_input)
                st.markdown("#### 📤 Raw Response")
                st.code(output, language="json")

                # Try to clean and complete JSON
                json_start = output.find("{")
                json_end = output.rfind("}") + 1
                json_str = output[json_start:json_end]
                json_str = json_str.replace("\n", "").replace("\r", "").replace("\\", "")

                # Patch partial endings
                if not json_str.strip().endswith("}"):
                    if json_str.strip().endswith(","):
                        json_str = json_str.rstrip(",")
                    if json_str.count("{") > json_str.count("}"):
                        json_str += "}"
                    if json_str.count("[") > json_str.count("]"):
                        json_str += "]}"

                try:
                    parsed = json.loads(json_str)
                    st.success("✅ Analysis Complete")
                    st.json(parsed)
                    st.download_button(
                        "📥 Download JSON",
                        json.dumps(parsed, indent=2),
                        file_name="fineprint_analysis.json",
                        mime="application/json"
                    )
                except Exception:
                    st.warning("⚠️ Couldn't parse clean JSON. Showing best attempt:")
                    st.code(json_str, language="json")

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
