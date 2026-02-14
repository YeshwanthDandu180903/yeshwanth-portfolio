# Security Policy

## 🔒 API Key Protection

This project uses external APIs (Groq, HuggingFace) which require secret keys. These keys **must never be committed to version control**.

### 1. Environment Variables
We use `python-dotenv` to manage sensitive configuration. 
- All API keys are stored in a `.env` file in the root directory.
- The `.env` file is excluded from git via `.gitignore`.

### 2. Setup Instructions for Contributors
To run this project locally, you must create your own `.env` file:

1. Copy the example template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your keys:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

### 3. Deployment Security
When deploying this application (e.g., to Render, Vercel, or AWS):
- Do **not** upload the `.env` file.
- Set the environment variables directly in your hosting provider's dashboard/settings.

## 🚫 Restricted Files
The following files are strictly ignored by git to prevent accidental exposure of sensitive data:
- `.env`
- `api.txt`
- `portfolio/` (internal builds)
- `__pycache__/`

If you discover a security vulnerability or have concerns about an exposed key, please contact the repository owner immediately or rotate your keys.
