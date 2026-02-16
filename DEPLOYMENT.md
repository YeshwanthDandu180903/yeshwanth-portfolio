# Zero-Cost Deployment Guide 🚀

This guide explains how to deploy your **RAG Chatbot Backend** to Hugging Face Spaces (High RAM, Free) and your **Frontend** to GitHub Pages/Vercel.

## Phase 1: Deploy Backend (Hugging Face Spaces)

1.  **Push Code to GitHub**:
    *   Commit and push all your latest changes to your GitHub repository.

2.  **Create Space**:
    *   Go to [Hugging Face Spaces](https://huggingface.co/spaces).
    *   Click **Create new Space**.
    *   **Space Name**: `portfolio-backend` (or similar).
    *   **License**: `MIT` (optional).
    *   **SDK**: Select **Docker** (⚠️ NOT Gradio) - We created a `Dockerfile` specifically for this.
    *   **Space Hardware**: `CPU Basic` (Free) - This gives you 16GB RAM!

3.  **Connect Repo**:
    *   After creating, it might ask to sync with GitHub or upload files.
    *   Since you selected Docker, it expects a `Dockerfile`.
    *   You can connect your GitHub repository directly so updates are automatic.

4.  **Add API Key**:
    *   Go to **Settings** tab in your Space.
    *   Scroll to **Variables and secrets**.
    *   Click **New Secret**.
    *   Name: `GROQ_API_KEY`
    *   Value: (Paste your Groq API Key)

5.  **Get Backend URL**:
    *   Once the Space is "Building" and then "Running", look for the **Direct URL**.
    *   It usually looks like: `https://yourusername-spacename.hf.space`
    *   Copy this URL.

---

## Phase 2: Connect Frontend

1.  **Update Config**:
    *   Open `js/config.js` in your local code.
    *   Paste your Copied Backend URL into the `API_URL` variable.
    *   *Example*:
        ```javascript
        const CONFIG = {
            // ...
            API_URL: 'https://yeshu1809-portfolio-backend.hf.space' 
        };
        ```

2.  **Push Config**:
    *   Commit and push this change to GitHub.

---

## Phase 3: Deploy Frontend (Vercel or GitHub Pages)

### Option A: Vercel (Recommended)
1.  Go to Vercel -> **Add New Project**.
2.  Import your GitHub Repository.
3.  Click **Deploy**.
4.  Vercel will build your site and give you a public URL (e.g., `yeshwanth-portfolio.vercel.app`).

### Option B: GitHub Pages
1.  Go to your Repo Settings -> **Pages**.
2.  Select `main` branch -> `/root` (or `/docs` if you moved files).
3.  Save.

---

## Testing
1.  Open your **Frontend URL** (e.g., Vercel link).
2.  Open the Chatbot.
3.  Ask "Tell me about your AI projects".
4.  It should connect to your Hugging Face backend and reply!

## Troubleshooting
*   **CORS Error**: If the chatbot doesn't reply, check the Console (F12). If you see "CORS block", ensure your `rag_backend/main.py` has `allow_origins=["*"]` (It currently does, so you should be safe).
*   **"Internal Server Error"**: Check the **Logs** tab in your Hugging Face Space.
