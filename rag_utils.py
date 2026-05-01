import os
import tempfile

from dotenv import load_dotenv

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

VECTOR_STORE_PATH = "vector_store"
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = None


# 📌 Process uploaded files
def process_files(files, chunk_size=1000, chunk_overlap=100):
    global vector_db

    docs = []

    for file in files:
        ext = os.path.splitext(file.name)[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        if ext == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif ext == ".csv":
            loader = CSVLoader(tmp_path)
        elif ext == ".txt":
            loader = TextLoader(tmp_path)
        else:
            continue

        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(docs)

    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_STORE_PATH)


# 📌 Ask question (modern LCEL chain)
def ask_question(query, k=3):
    global vector_db

    #
    # if vector_db is None:
    #     vector_db = FAISS.load_local(
    #         VECTOR_STORE_PATH,
    #         embeddings,
    #         allow_dangerous_deserialization=True
    #     )
    #
    if vector_db is None:
        return "Please process files first", []
    #

    retriever = vector_db.as_retriever(search_kwargs={"k": k})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        "Answer the question based only on the context:\n\n{context}\n\nQuestion: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke(query)

    return result, []