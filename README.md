

````markdown
# 🔐 SecureMidea – Instagram Political Comment Filter

SecureMidea is a Chrome extension + FastAPI backend powered by a Hugging Face NLP model that detects and flags politically-influential or botnet-generated Arabic comments on Instagram posts and reels. 

The goal is to protect users from political manipulation and propaganda using AI-driven content moderation tools.

---

## 📌 Features

✅ Real-time extraction of Instagram comments and replies  
✅ Automatically detects comments while scrolling  
✅ Sends extracted text to a backend API for analysis  
✅ Uses an NLP model trained on Arabic political content (based on `aubmindlab/bert-base-arabertv02`)  
✅ Flags and highlights potentially manipulative political comments in red  
✅ Smooth, non-intrusive user experience on desktop

---

## 🚀 Project Structure

```bash
securemidea/
├── extension/
│   ├── manifest.json
│   └── content.js
│
├── backend/
│   └── main.py
│
├── README.md
└── requirements.txt
````

---

## 🧠 AI Model

* Model: [`aubmindlab/bert-base-arabertv02`](https://huggingface.co/aubmindlab/bert-base-arabertv02)
* Platform: Hugging Face Transformers
* Task: Text classification
* Trained on: Political Arabic content (custom fine-tuning planned)

---

## 💡 How It Works

1. The **Chrome extension** injects a script into Instagram.
2. It detects and extracts comments + replies in real time.
3. Comments are sent to a **FastAPI backend**.
4. The backend uses the Hugging Face model to classify text.
5. If a comment is marked as political, it is underlined in red directly on Instagram.

---

## 🛠️ Setup Guide

### 1. Backend (FastAPI + Hugging Face)

```bash
# Clone repo and navigate
git clone https://github.com/yourusername/securemidea.git
cd securemidea/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Run server
uvicorn main:app --reload --port 8000
```

* Your API will be running at: `http://localhost:8000/analyze`
* You can test it using Postman or Curl.

### 2. Chrome Extension

```bash
cd securemidea/extension
```

1. Open Chrome → `chrome://extensions`
2. Enable **Developer Mode**
3. Click **"Load unpacked"**
4. Select the `extension/` folder
5. Navigate to Instagram and watch the AI magic ✨

---

## 🧪 API Example

**Endpoint**: `POST /analyze`

```json
{
  "text": "هذا التعليق يحتوي على توجهات سياسية"
}
```

**Response**:

```json
{
  "label": "LABEL_1",
  "score": 0.91,
  "is_political": true,
  "text_sample": "هذا التعليق يحتوي عل...",
  "warning": "For PowerShell testing, use Format-List instead of ConvertTo-Json"
}
```

---

## 🔒 Security Note

* CORS is enabled for development (`allow_origins=["*"]`).
* For production, restrict allowed origins explicitly.

---

## 📅 Roadmap

* [x] Build DOM extractor for comments/replies
* [x] Integrate Hugging Face model with FastAPI
* [x] Flag comments in real time
* [ ] Train custom political content classifier
* [ ] Deploy to cloud (API + extension publishing)

---

## 👤 Author

**Ahmad M.** – Cybersecurity Student | Jordan 🇯🇴


---

## 🧠 Credits

* [Hugging Face Transformers](https://huggingface.co)
* [FastAPI](https://fastapi.tiangolo.com)
* [Arabert Model by AUB Mind Lab](https://huggingface.co/aubmindlab/bert-base-arabertv02)

---

## 📜 License

MIT License – Use it, modify it, improve it — but don't spread propaganda 😉

```

