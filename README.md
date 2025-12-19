# 🪙 Akademi Crypto AI Chatbot

**Asisten Virtual Cerdas untuk Platform Edukasi Trading Crypto**

Project ini adalah implementasi Chatbot Customer Service berbasis AI yang dirancang untuk website **Akademi Crypto**. Bot ini menggunakan teknologi **RAG (Retrieval Augmented Generation)** untuk menjawab pertanyaan pengguna berdasarkan basis pengetahuan internal, bukan hanya mengarang jawaban.

Dibangun dengan **FastAPI** di backend dan **Vanilla JavaScript** di frontend dengan antarmuka Dark Mode yang modern.

---

## 🚀 Fitur Utama

* **🧠 AI Powered:** Menggunakan **Google Gemini 2.5 Flash** untuk pemahaman bahasa yang natural dan cepat.
* **📚 RAG Technology:** Menggunakan **LangChain** dan **FAISS** (Vector Database) untuk mencari jawaban akurat dari dokumen internal perusahaan.
* **💬 Context Aware:** Bot mengingat konteks percakapan sebelumnya menggunakan *Session ID* yang disimpan di local storage.
* **🎨 Modern UI:** Antarmuka *Dark Mode* dengan warna tema Ungu/Hitam yang responsif (Mobile Friendly).
* **📝 Markdown Support:** Bot dapat menampilkan format teks (bold, list, dll) menggunakan `marked.js`.
* **💾 Chat History:** Riwayat percakapan disimpan dalam format JSON di server untuk keperluan audit/logging.

---

## 🛠️ Teknologi yang Digunakan

### Backend
* **Python 3.11**
* **FastAPI:** Web framework untuk API yang cepat.
* **LangChain:** Framework untuk orkestrasi LLM.
* **Google GenAI (Gemini):** Model LLM utama.
* **HuggingFace Embeddings:** Model embedding multilingual (`paraphrase-multilingual-MiniLM-L12-v2`).
* **FAISS:** Vector Store untuk pencarian kesamaan (similarity search).

### Frontend
* **HTML5 & CSS3:** Desain responsif.
* **JavaScript (Vanilla):** Logika fetch API dan manajemen DOM.
* **Marked.js:** Library untuk merender format markdown dari bot.

---

## 📂 Struktur Project

```text
.
├── chatbot_backend.py     # Server utama FastAPI & Logika AI
├── chatbot_logic.js       # Logika Frontend (Fetch API & UI Interaksi)
├── index.html             # Landing Page Akademi Crypto
├── style.css              # Styling Website (Dark Mode)
├── training_knowledge.py  # (Diperlukan) Script untuk membuat vector database
├── faiss_index/           # (Auto-generated) Folder database vector
├── chat_logs/             # (Auto-generated) Folder riwayat chat user
├── logo-new-1-2-1.webp    # Aset Logo
├── .env                   # File konfigurasi API Key
└── requirements.txt       # Daftar library Python
