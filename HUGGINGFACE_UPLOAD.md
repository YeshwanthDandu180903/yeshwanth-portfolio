# Files to Upload to Hugging Face Space

## 📋 Upload Checklist

Upload these files/folders to your Hugging Face Space:

### ✅ Required Files (Root Level):
1. ✅ `Dockerfile` - Docker configuration
2. ✅ `requirements.txt` - Python dependencies  
3. ✅ `runtime.txt` - Python version (optional but recommended)

### ✅ Required Folder:
4. ✅ `rag_backend/` - **ENTIRE FOLDER** including:
   - `main.py`
   - `rag_agent.py`
   - `context_engineering_prompt_new_file.md`
   - `linkedin_prompt.md`
   - `faiss_index/` subfolder (with index.faiss and index.pkl)

## 🚫 Do NOT Upload:
- ❌ `data/` folder
- ❌ `scripts/` folder
- ❌ `_archive/` folder
- ❌ `css/`, `js/`, `images/` folders (these are for frontend only)
- ❌ `index.html` (frontend file)
- ❌ `.env` file (use Secrets instead)

## 📤 How to Upload:

### Method 1: Via Web Interface (Easiest)
1. Click **"Files"** tab at the top
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop:
   - `Dockerfile`
   - `requirements.txt`
   - `runtime.txt`
4. Click **"Add file"** → **"Upload folder"**
5. Select the entire `rag_backend` folder

### Method 2: Via Git (Advanced)
Run these commands from your portfolio directory:

```bash
# Add Hugging Face as remote
git remote add huggingface https://huggingface.co/spaces/Yeshu1809/portfolio-backend

# Create a new branch with only backend files
git checkout -b huggingface-deploy

# Remove frontend files (they won't be deleted from your local repo)
git rm -r --cached css/ js/ images/ index.html

# Commit
git commit -m "Deploy backend to Hugging Face"

# Push to Hugging Face
git push huggingface huggingface-deploy:main

# Switch back to main branch
git checkout main
```

## 🔑 After Upload: Add Secret

1. Go to **Settings** tab
2. Find **"Repository secrets"**
3. Click **"New secret"**
4. Add:
   - Name: `GROQ_API_KEY`
   - Value: (paste from your .env file)

## ✅ Verification

After upload, your Hugging Face Space should show:
```
portfolio-backend/
├── Dockerfile
├── requirements.txt
├── runtime.txt
└── rag_backend/
    ├── main.py
    ├── rag_agent.py
    ├── context_engineering_prompt_new_file.md
    ├── linkedin_prompt.md
    └── faiss_index/
        ├── index.faiss
        └── index.pkl
```

The Space will automatically start building once you upload the Dockerfile!
