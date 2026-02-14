# Yeshwanth Dandu | Data Scientist Portfolio 🚀

Welcome to the source code of my personal portfolio website! This project showcases my journey as a Data Scientist, featuring my projects, skills, experience, and an **AI-powered RAG Chatbot** capable of answering questions about my professional background.

![Portfolio Preview](images/personal/my_photo.jpeg) 
*(Note: Replace with a screenshot of the landing page if available)*

## 🌟 Features

- **Responsive Design**: Fully responsive layout optimized for Desktop, Tablet, and Mobile devices.
- **Dark/Light Theme**: Seamless toggle between dark and light modes for comfortable viewing.
- **Interactive UI**: Glassmorphism effects, typing animations, and smooth scrolling for a premium user experience.
- **AI Chatbot Agent**:
  - Built with **RAG (Retrieval-Augmented Generation)** architecture.
  - Answers questions about my resume, projects, and skills.
  - Powered by **Groq (Llama-3)** and **LangChain**.
  - Uses **FAISS** for efficient vector similarity search.
- **Dynamic Content**: Sections for About, Experience, Education, Projects, and Skills.

## 🛠️ Tech Stack

### Frontend
- **HTML5 & CSS3**: Semantic HTML with Custom CSS and Bootstrap 5.
- **JavaScript**: Vanilla JS for DOM manipulation, animations, and API integration.
- **Styling**: Glassmorphism design system, CSS Variables for theming.

### Backend (AI Agent)
- **Python**: Core logic for the chatbot and data processing.
- **Flask**: Lightweight web server to expose the Chat API.
- **LangChain**: Framework for building the RAG application.
- **Groq API**: Interface for the Llama-3 LLM.
- **HuggingFace Embeddings**: `all-MiniLM-L6-v2` for generating text embeddings.
- **FAISS**: Vector database for storing and retrieving document chunks.

## 📂 Project Structure

```bash
portfolio/
├── css/                  # Stylesheets (style.css, chat.css)
├── js/                   # JavaScript files
├── images/               # Static assets and project screenshots
├── faiss_index/          # Local vector store (FAISS index)
├── app.py                # Flask API server for the Chatbot
├── rag_agent.py          # Core RAG Agent logic (LangChain + Groq)
├── build_vector_store.py # Script to ingest PDF and build FAISS index
├── index.html            # Main entry point
├── .env                  # Environment variables (API Keys)
└── requirements.txt      # Python dependencies
```

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YeshwanthDandu180903/portfolio.git
   cd portfolio
   ```

2. **Create a virtual environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If `requirements.txt` is missing, install the core packages manually:*
   ```bash
   pip install flask flask-cors python-dotenv groq langchain langchain-community langchain-huggingface faiss-cpu pypdf
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### 🏃‍♂️ Running the Application

This project consists of two parts: the **Frontend** (HTML/JS) and the **Backend** (Flask API).

#### 1. Start the Backend Server (Chatbot API)
Run the Flask app to serve the AI agent:
```bash
python app.py
```
*The API will start at `http://localhost:5000`.*

#### 2. Serve the Frontend
You can open `index.html` directly, but for best results (and to avoid CORS issues if not configured), use a simple HTTP server:

Open a new terminal configuration:
```bash
python -m http.server 8000
```
*Access the portfolio at `http://localhost:8000`.*

## 🧠 AI Agent Workflow

1. **Data Ingestion**: The `build_vector_store.py` script reads `pdf_content.txt` (extracted from Resume/Project docs).
2. **Embedding**: Text is split into chunks and embedded using HuggingFace models.
3. **Indexing**: Embeddings are stored in a local FAISS index.
4. **Retrieval**: When a user asks a question, the system finds relevant chunks from the FAISS index.
5. **Generation**: The retrieved context + user query are sent to the Groq LLM to generate an accurate, context-aware response.

## 📬 Contact

- **Email**: [yeshwanthdandu2003@gmail.com](mailto:yeshwanthdandu2003@gmail.com)
- **LinkedIn**: [Yeshwanth Dandu](https://linkedin.com/in/yeshwanthdandu)
- **GitHub**: [YeshwanthDandu180903](https://github.com/YeshwanthDandu180903)

---

&copy; 2026 Yeshwanth Dandu. All Rights Reserved.
