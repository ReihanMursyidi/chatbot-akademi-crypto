// ==========================================
// LOGIKA CHATBOT AKADEMI CRYPTO (VERSI FORM)
// ==========================================

// 1. SETUP SESSION ID
let sessionId = localStorage.getItem('chatbot_session_id');
if (!sessionId) {
    sessionId = "user_" + Date.now();
    localStorage.setItem('chatbot_session_id', sessionId);
}

// 2. MUAT HISTORY SAAT WEBSITE SIAP
document.addEventListener("DOMContentLoaded", function() {
    
    // --- LOAD HISTORY ---
    loadHistory();

    // --- SETUP MANUAL TOMBOL ENTER ---
    // Kita pasang "telinga" di kolom input
    const inputField = document.getElementById("userInput");
    
    if (inputField) {
        inputField.addEventListener("keydown", function(event) {
            // Cek apakah tombol yang ditekan adalah ENTER
            if (event.key === "Enter") {
                event.preventDefault(); // MATIKAN FUNGSI BAWAAN (REFRESH)
                console.log("Tombol Enter ditekan. Mencegah Refresh..."); // Cek Console
                sendMessage(); // JALANKAN FUNGSI KIRIM
            }
        });
    }
});

// FUNGSI LOAD HISTORY
async function loadHistory() {
    try {
        const response = await fetch(`https://unremaining-unmanipulatory-porter.ngrok-free.dev/history/${sessionId}`);
        if (!response.ok) return;

        const history = await response.json();
        const chatBody = document.getElementById('chatBody');

        if (history && history.length > 0) {
            history.forEach(item => {
                if (!item.message) return;
                let cssClass = (item.role === "user") ? "msg-user" : "msg-bot";
                let content = item.message;

                if (item.role === "bot" && typeof marked !== 'undefined') {
                    content = marked.parse(content);
                }
                chatBody.innerHTML += `<div class="msg ${cssClass}">${content}</div>`;
            });
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    } catch (error) {
        console.error("History error:", error);
    }
}

// 3. FUNGSI BUKA/TUTUP CHAT
function toggleChat() {
    const w = document.getElementById('chatWindow');
    if (w.style.display === 'flex') {
        w.style.display = 'none';
    } else {
        w.style.display = 'flex';
        setTimeout(() => {
            const input = document.getElementById('userInput');
            if(input) input.focus();
            const body = document.getElementById('chatBody');
            if(body) body.scrollTop = body.scrollHeight;
        }, 100);
    }
}

// 4. FUNGSI KIRIM PESAN (Simple, tidak perlu handle Enter lagi)
async function sendMessage() {
    const inputField = document.getElementById('userInput');
    const chatBody = document.getElementById('chatBody');
    const question = inputField.value.trim();

    if (!question) return;

    // A. Tampilkan Pesan User
    chatBody.innerHTML += `<div class="msg msg-user">${question}</div>`;
    inputField.value = ''; // Kosongkan input
    chatBody.scrollTop = chatBody.scrollHeight;

    // B. Loading
    const loadingId = "loading-" + Date.now();
    chatBody.innerHTML += `<div class="msg msg-bot" id="${loadingId}">...</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        const response = await fetch('https://unremaining-unmanipulatory-porter.ngrok-free.dev/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: question,
                session_id: sessionId
            })
        });

        const data = await response.json();
        
        const loader = document.getElementById(loadingId);
        if(loader) loader.remove();

        let botAnswer = data.answer;
        if (typeof marked !== 'undefined') {
            botAnswer = marked.parse(botAnswer);
        }

        chatBody.innerHTML += `<div class="msg msg-bot">${botAnswer}</div>`;

    } catch (error) {
        const loader = document.getElementById(loadingId);
        if(loader) loader.innerText = "❌ Error koneksi";
    }

    chatBody.scrollTop = chatBody.scrollHeight;
}