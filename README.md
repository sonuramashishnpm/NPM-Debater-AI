# 🤖 NPM A.I - Infinite Debate Arena

[![Live Demo](https://img.shields.io)](https://npmdebateai.onrender.com)
[![Python](https://img.shields.io)](https://www.python.org)
[![Flask](https://img.shields.io)](https://flask.palletsprojects.com)

An interactive, real-time debate platform where four powerful LLMs (**Llama 3.2, Qwen 2.5, Mistral 7B, and Vicuna 7B**) clash in an infinite loop of logic and persuasion. 

**Explore the Arena:** [https://npmdebateai.onrender.com](https://npmdebateai.onrender.com)

---

## 🚀 Features

-   **Real-Time NDJSON Streaming:** Uses a custom `yield` architecture to push AI responses to the frontend one-by-one. No more waiting for the entire debate to finish!
-   **Multi-Model Intelligence:** Using `npmai` we combined the unique personalities of Llama, Qwen, Mistral, and Vicuna.
-   **Sequential Context:** Each AI listens to the previous speakers before formulating its unique point of view.
-   **Persistent Memory:** Integrated memory management that saves debate history to disk, allowing AIs to remember previous rounds.
-   **Cyberpunk Glassmorphism UI:** A sleek, dark-themed interface with background video support and responsive grid layouts.
-   **No Signup/Sigin:* We believe that we are providing in free and to save your time and privacy we do not ask your any personal information.

---

## 🛠️ Tech Stack

-   **Backend:** [Flask](https://flask.palletsprojects.com) (Python)
-   **AI Core:** [Ollama](https://ollama.com) & `npmai` library
-   **Streaming:** `stream_with_context` (Server-Sent Data)
-   **Frontend:** JavaScript [Fetch ReadableStream API](https://developer.mozilla.org), HTML5, CSS3

---

## 📥 Local Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/sonuramashishnpm/NPM-Debater-AI.git
   cd npm-debate-ai
