# main_app.py

import tempfile
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from utils import load_whisper_model, load_gemini_llm
from prompts import PREDEFINED_INTENTS
from processor import process_call

# ─── Streamlit Config ─────────────────
st.set_page_config(page_title="Call Quality Assurance", layout="wide")
DEBUG = False

# ─── Load Models ──────────────────────
whisper_model = load_whisper_model("medium")
gemini_llm    = load_gemini_llm("gemini-2.5-flash-preview-04-17")

def run():
    st.title("📞 Multi-Language Call Quality Assurance")

    uploads = st.file_uploader(
        "🎧 Upload audio files", type=["mp3","wav","m4a"], accept_multiple_files=True
    )

    st.markdown("### 🎯 Select Intents")
    cols = st.columns(4)
    selected = [
        intent for idx, intent in enumerate(PREDEFINED_INTENTS)
        if cols[idx % 4].checkbox(intent, False)
    ]
    custom = st.text_input("➕ Custom intents (comma-separated)")
    if custom:
        selected += [c.strip() for c in custom.split(",") if c.strip()]

    # Initialize session-state keys if missing
    if "summaries" not in st.session_state:
        st.session_state.summaries = {}
    if "selected_summary" not in st.session_state:
        st.session_state.selected_summary = None

    df = None  # placeholder for results DataFrame

    # ─── Run Analysis ─────────────────────────
    if st.button("🚀 Run Analysis") and uploads:
        # Reset state for new run
        st.session_state.summaries = {}
        st.session_state.selected_summary = None

        results, errors = [], []
        prog = st.progress(0)
        status = st.empty()

        for i, f in enumerate(uploads, start=1):
            status.text(f"🔄 Processing {f.name} ({i}/{len(uploads)})")

            # Save upload to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.name).suffix) as tf:
                tf.write(f.read())
                temp_path = tf.name

            try:
                row, summary = process_call(
                    temp_path, whisper_model, gemini_llm, selected, debug=DEBUG
                )
                row["File Name"] = f.name
                results.append(row)
                st.session_state.summaries[f.name] = summary

            except Exception as e:
                errors.append(f"{f.name} → {e}")

            prog.progress(i / len(uploads))
            time.sleep(0.1)

        # Build DataFrame
        df = pd.DataFrame(results)

        st.success("✅ All done!")
        st.dataframe(df, use_container_width=True)

        if errors:
            st.error("Errors:")
            for e in errors:
                st.write(f"- {e}")

    elif not uploads:
        st.info("Please upload audio files to begin.")
    else:
        st.info("Select intents then click Run Analysis.")

    # ─── View Summaries Section ─────────────────────────
    if st.session_state.summaries:
        st.markdown("---")
        st.header("📝 View Summaries")

        if st.session_state.selected_summary is None:
            # List all summary buttons
            for fn in st.session_state.summaries.keys():
                if st.button(f"📝 View Summary: {fn}", key=f"view_{fn}"):
                    st.session_state.selected_summary = fn
        else:
            # Display selected summary with back button
            summ = st.session_state.summaries.get(
                st.session_state.selected_summary,
                "Summary not available."
            )
            st.markdown(f"### Summary for {st.session_state.selected_summary}")
            st.markdown(summ.replace("\n", "  \n"))

            if st.button("🔙 Back to Summaries"):
                st.session_state.selected_summary = None

    # ─── Download Report ─────────────────────────
    if df is not None and not df.empty:
        st.markdown("---")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_fn = f"call_qc_report_{ts}.xlsx"
        df.to_excel(out_fn, index=False)
        with open(out_fn, "rb") as fp:
            st.download_button(
                "📥 Download Report",
                fp,
                file_name=out_fn,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    run()
