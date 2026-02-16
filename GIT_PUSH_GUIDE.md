# Git Push Checklist for Deployment

## ✅ Files TO PUSH (Required for Deployment)

### Frontend Files
- ✅ `index.html`
- ✅ `css/style.css`
- ✅ `css/chat.css`
- ✅ `js/main.js`
- ✅ `js/chat.js`
- ✅ `js/config.js` (NEW - API configuration)
- ✅ `images/` folder

### Backend Files
- ✅ `rag_backend/main.py`
- ✅ `rag_backend/rag_agent.py`
- ✅ `rag_backend/context_engineering_prompt_new_file.md`
- ✅ `rag_backend/linkedin_prompt.md`
- ✅ `rag_backend/faiss_index/` (Vector database)

### Deployment Configuration
- ✅ `Dockerfile` (for Hugging Face Spaces)
- ✅ `Procfile` (backup for Render/Heroku)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `runtime.txt` (Python version)
- ✅ `.gitignore` (updated)

### Documentation
- ✅ `README.md`
- ✅ `DEPLOYMENT.md` (NEW - deployment guide)
- ✅ `LICENSE`
- ✅ `SECURITY.md`

## ❌ Files NOT TO PUSH (Excluded by .gitignore)

- ❌ `_archive/` - Old/backup files
- ❌ `data/` - PDF and extracted text (contains api.txt)
- ❌ `scripts/` - Build scripts (not needed in production)
- ❌ `faiss_index/` (root level - duplicate)
- ❌ `portfolio/` - Virtual environment
- ❌ `.env` - Environment variables
- ❌ `temp_*.css`, `temp_*.html` - Temporary files
- ❌ `fix_*.py` - Temporary Python scripts

## 📋 Git Commands to Execute

```bash
# 1. Check current status
git status

# 2. Add all required files (gitignore will automatically exclude unwanted files)
git add .

# 3. Check what will be committed
git status

# 4. Commit with descriptive message
git commit -m "feat: Add RAG chatbot backend and deployment configs

- Added Dockerfile for Hugging Face Spaces deployment
- Updated backend with lazy-loading vector store
- Added config.js for API URL management
- Updated .gitignore to exclude archive and data folders
- Added deployment documentation"

# 5. Push to GitHub
git push origin main
```

## 🔍 Verification Steps

After pushing, verify on GitHub:
1. Check that `_archive/`, `data/`, `scripts/` folders are NOT visible
2. Verify `rag_backend/faiss_index/` IS present
3. Confirm `Dockerfile` and `requirements.txt` are present
4. Ensure `.env` and `api.txt` are NOT visible

## 🚀 Next Steps After Push

1. **Hugging Face Spaces**: Create new Space with Docker SDK
2. **Add Secret**: Add `GROQ_API_KEY` in Space settings
3. **Vercel**: Import GitHub repo and deploy frontend
4. **Update config.js**: Add your Hugging Face Space URL
