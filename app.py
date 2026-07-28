from pathlib import Path

import streamlit as st

from research_copilot.pipeline import ResearchCopilot

st.set_page_config(page_title="Research Copilot", page_icon="🔎", layout="wide")
st.title("Research Intelligence Copilot")
st.caption("Ask grounded questions across your research documents.")


@st.cache_resource
def get_copilot() -> ResearchCopilot:
    return ResearchCopilot()


copilot = get_copilot()

with st.sidebar:
    st.header("Knowledge base")
    source_path = st.text_input("Document directory", "data/sample_docs")
    if st.button("Build index", use_container_width=True):
        try:
            result = copilot.ingest(Path(source_path))
            st.success(f"Indexed {result.documents} documents into {result.chunks} chunks.")
        except (FileNotFoundError, ValueError) as error:
            st.error(str(error))

question = st.text_input("Question", placeholder="How should a RAG system be evaluated?")
top_k = st.slider("Retrieved chunks", min_value=1, max_value=8, value=4)

if st.button("Ask", type="primary", disabled=not question):
    response = copilot.query(question, top_k)
    st.subheader("Answer")
    st.markdown(response.answer)
    st.metric("Retrieval confidence", f"{response.confidence:.2f}")

    if response.citations:
        st.subheader("Sources")
        for citation in response.citations:
            page = f" · page {citation.page}" if citation.page else ""
            with st.expander(f"{citation.source}{page} · {citation.chunk_id}"):
                st.write(citation.excerpt)
