import streamlit as st
from utils.compare import load_notebook, compare_notebooks, compute_creativity_score
from utils.ai_detection import detect_ai_in_cells

st.title("📘 Notebook Comparator - AI Detection & Creativity Score")

orig_file = st.file_uploader("Upload Original Notebook (.ipynb)", type=["ipynb"])
test_file = st.file_uploader("Upload Modified Notebook (.ipynb)", type=["ipynb"])

if orig_file and test_file:
    with st.spinner("🔍 Processing..."):
        orig_cells = load_notebook(orig_file)
        test_cells = load_notebook(test_file)

        diffs = compare_notebooks(orig_cells, test_cells)
        creativity = compute_creativity_score(diffs)

        st.header("🔬 Differences")
        for i, (tag, orig, test) in enumerate(diffs):
            st.markdown(f"**{i+1}. Change Type:** `{tag}`")
            if orig:
                st.code("\n".join(orig), language='python')
            if test:
                st.code("\n".join(test), language='python')
            st.markdown("---")

        st.success(f"🎨 Creativity Score: {creativity}/100")

        st.subheader("🤖 AI Detection (via GPT)")
        ai_results = detect_ai_in_cells([test for tag, _, test in diffs if test])

        ai_count = sum(1 for r in ai_results if "AI-generated" in r)
        st.info(f"{ai_count} of {len(ai_results)} changed cells likely AI-generated")

        for idx, result in enumerate(ai_results):
            st.markdown(f"**Cell {idx+1} Judgment:** {result}")

