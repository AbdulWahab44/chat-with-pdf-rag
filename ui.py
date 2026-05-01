import streamlit as st
from rag_utils import process_files, ask_question

st.set_page_config(page_title="RAG App", layout="wide")

st.title("📄 Chat with your Files | RAG")

# Sidebar
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF/CSV/TXT",
    type=["pdf", "csv", "txt"],
    accept_multiple_files=True
)

chunk_size = st.sidebar.number_input("Chunk Size", 500, 3000, 1000)
chunk_overlap = st.sidebar.number_input("Chunk Overlap", 0, 500, 100)
top_k = st.sidebar.number_input("Top K", 1, 10, 3)

if st.sidebar.button("Process Files"):
    if uploaded_files:
        with st.spinner("Processing files..."):
            process_files(uploaded_files, chunk_size, chunk_overlap)
        st.success("Files processed successfully!")
    else:
        st.warning("Upload files first")

# Main area
st.subheader("Ask Question")

query = st.text_input("Type your question")

if st.button("Ask"):
    if query:
        with st.spinner("Thinking..."):
            answer, _ = ask_question(query, top_k)

        st.write("### Answer")
        st.write(answer)
    else:
        st.warning("Enter a question")