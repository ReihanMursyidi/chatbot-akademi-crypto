from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_MODEL = "gemini-2.5-flash"

# SETUP: LOAD DATABASE & AI
print("🔄 Memuat basis pengetahuan...")

# Gunakan Model Embedding Lokal
embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

vectorstore = None


try:
    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        # Setup Retreiver (Pencari data)
        retriever = vectorstore.as_retriever()

        llm = ChatGoogleGenerativeAI(model=CURRENT_MODEL, temperature=0.3)

        template_instructions = f"""Anda adalah AI Customer Service Akademi Crypto yang cerdas.
        
        INFORMASI SISTEM:
        Saat ini Anda sedang beroperasi menggunakan model arsitektur: {CURRENT_MODEL}.
        Jika pengguna bertanya "model apa yang digunakan?" atau "siapa kamu?", 
        jawablah dengan menyebutkan bahwa Anda menggunakan {CURRENT_MODEL}.
        Jelaskan juga model yang sedang digunakan ini adalah model yang seperti apa dengan jelas dan singkat.

        TUGAS:
        Gunakan potongan konteks berikut untuk menjawab pertanyaan pengguna.
        Jika Anda tidak tahu jawabannya dari konteks, katakan saja tidak tahu, jangan mengarang.
        
        Konteks:
        {{context}}

        Pertanyaan: {{question}}

        Jawaban yang Bermanfaat:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template_instructions)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        print("✅ Basis pengetahuan berhasil dimuat.")
    else:
        qa_chain = None
        print("File 'faiss_index' tidak ditemukan. Jalankan training_knowledge.py terlebih dahulu.")

except Exception as e:
    qa_chain = None
    print(f"❌ Gagal memuat basis pengetahuan: {e}")

# --- FUNGSI LOGGING ---
LOG_FOLDER = "chat_logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

def save_to_log(session_id, role, message):
    filename = f"{LOG_FOLDER}/chat_{session_id}.json"

    # Baca log yang ada
    history = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

    # Tambah pesan baru
    history.append({"role": role, "message": message})

    # Simpan kembali ke file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

# STRUKTUR DATA REQUEST
class Question(BaseModel):
    question: str
    session_id: str

# ENDPOINT UTAMA
@app.post("/chat")
async def chat(request: Question):
    if not qa_chain:
        raise HTTPException(status_code=500, detail="Database belum siap/rusak.")
    
    try:
        # Simpan pertanyaan user ke log
        save_to_log(request.session_id, "user", request.question)

        # Kirim pertanyaan ke chain
        response = qa_chain.invoke({"query": request.question})
        answer = response['result']

        # Simpan jawaban bot ke log
        save_to_log(request.session_id, "bot", answer)

        return {"answer": answer}
    
    except Exception as e:
        return {"answer": "Maaf, terjadi kesalahan sistem.", "error": str(e)}
    
@app.get("/history/{session_id}")
def get_history(session_id: str):
    filename = f"{LOG_FOLDER}/chat_{session_id}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []