
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
            from langchain_community.embeddings import FastEmbedEmbeddings
            
            # Load index from the faiss_index sibling directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            index_path = os.path.join(current_dir, "faiss_index")
            
            if not os.path.exists(index_path):
                print(f"Index not found at {index_path}. Attempting to look in parent directory rag_backend/faiss_index...")
                # Fallback for some deployment structures or running from root
                root_dir = os.path.dirname(current_dir) # parent of rag_backend
                index_path = os.path.join(root_dir, "rag_backend", "faiss_index")

            self.embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
            # Allow dangerous deserialization because we created the index ourselves locally
            self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
            print("Vector store loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load vector store: {e}")
            self.vector_store = None

    def _load_system_prompt(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "context_engineering_prompt_new_file.md")
            
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful assistant for Yeshwanth's portfolio."

    def _load_linkedin_prompt(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "linkedin_prompt.md")
            
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful assistant for generating LinkedIn content."

    def generate_linkedin_content(self):
        # Ensure resources are loaded
        self._lazy_load()
        
        # Load the specific LinkedIn prompt
        system_prompt = self._load_linkedin_prompt()
        
        context = ""
        if self.vector_store:
            try:
                # Query for relevant recent updates or core projects
                # We use a broad query to get a good mix of recent and relevant info
                docs = self.vector_store.similarity_search("recent AI projects RAG systems deployment learning", k=4)
                context = "\n\n".join([doc.page_content for doc in docs])
            except Exception as e:
                print(f"Error retrieving context for LinkedIn content: {e}")
        
        # Enhance system prompt with context
        if context:
            system_prompt += f"\n\n## RELEVANT PORTFOLIO CONTEXT:\n{context}\n\n"
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": "Generate the LinkedIn content previews now.",
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error interacting with the AI: {str(e)}"

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
                docs = self.vector_store.similarity_search(user_query, k=6)
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
