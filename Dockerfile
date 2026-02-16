
# 2025: Hugging Face Spaces (Generous Free Tier)
# This setup is perfect for deploying your RAG chatbot with plenty of RAM (16GB)
# for free, compared to Render's limited RAM.

FROM python:3.9-slim

WORKDIR /app

# Create a non-root user for security (required by some cloud providers)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements from current directory
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the backend code (includes faiss_index inside rag_backend/)
COPY --chown=user rag_backend ./rag_backend


# Expose the port used by Hugging Face Spaces
EXPOSE 7860

# Command to run the application
# We point to rag_backend.main and run on port 7860
CMD ["uvicorn", "rag_backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
