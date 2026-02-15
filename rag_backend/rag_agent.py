
import os
from groq import Groq
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

class PortfolioAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = Groq(api_key=self.api_key)
        self.system_prompt = self._load_system_prompt()
        
        # Initialize as None for lazy loading
        self.embeddings = None
        self.vector_store = None
        print("Agent initialized. Resources will be loaded on first request.")

    def _lazy_load(self):
        if self.vector_store is not None:
            return

        print("Lazy loading vector store...")
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            # Allow dangerous deserialization because we created the index ourselves locally
            self.vector_store = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
            print("Vector store loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load vector store: {e}")
            self.vector_store = None

    def _load_system_prompt(self):
        try:
            with open("context_engineering_prompt.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful assistant for Yeshwanth's portfolio."

    def get_response(self, user_query):
        # Ensure resources are loaded
        self._lazy_load()
        
        # Reload prompt for development agility
        self.system_prompt = self._load_system_prompt()
        
        context = ""
        context_sources = []
        if self.vector_store:
            try:
                # Retrieve top 3 chunks
                docs = self.vector_store.similarity_search(user_query, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
            except Exception as e:
                print(f"Error retrieving context: {e}")
        
        # Enhance system prompt with context if available
        final_system_prompt = self.system_prompt
        if context:
            final_system_prompt += f"\n\n## RELEVANT CONTEXT FROM RESUME/PORTFOLIO:\n{context}\n\n"
        
        # Append strict formatting instruction at the very end to ensure adherence
        final_system_prompt += f"""
        
        ## INSTRUCTION FOR RESPONSE:
        User Question: "{user_query}"
        
        Using the above context (if relevant) and your general knowledge, answer the question.
        
        CRITICAL: 
        1. DO NOT USE MARKDOWN BOLDING (**text**). 
        2. DO NOT USE MARKDOWN HEADERS (# Header).
        3. Use simple hyphens (-) for lists.
        4. Keep it clean and readable as plain text.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": final_system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model="llama-3.3-70b-versatile", # Updated to a currently active model
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error interacting with the AI: {str(e)}"

if __name__ == "__main__":
    # fast test
    try:
        agent = PortfolioAgent()
        print("Agent initialized. Type 'quit' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            response = agent.get_response(user_input)
            print(f"AI: {response}")
    except ValueError as e:
        print(e)
