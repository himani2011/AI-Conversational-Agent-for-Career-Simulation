from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector DB
vectorstore = FAISS.load_local(
    "rag/vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()

# Load local LLM
llm = pipeline(
    "text-generation",
    model="microsoft/phi-2",
    max_new_tokens=200,
    temperature=0.5
)

def ask_career_bot(question):
    # Step 1: Retrieve docs
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])

    # Step 2: Strong prompt (forces answer only)
    prompt = f"""
You are an AI Career Coach.

Answer the question using the context below.
Give ONLY the final answer.
Do NOT repeat the question.
Do NOT include the words Context or Question.

Context:
{context}

Question:
{question}

Answer:
"""

    # Step 3: Generate
    response = llm(prompt)
    raw_output = response[0]['generated_text']

    # Step 4: Clean output (important fix)
    if "Answer:" in raw_output:
        clean_output = raw_output.split("Answer:")[-1].strip()
    else:
        # fallback: take last 2–3 lines only
        clean_output = raw_output.strip().split("\n")[-3:]
        clean_output = " ".join(clean_output).strip()

    return clean_output