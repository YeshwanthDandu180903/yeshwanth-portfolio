
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
                model="llama-3.3-8b",
                temperature=0.5,
                max_tokens=512,
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
        
        CRITICAL TOKEN-SAVING RULES:
        1. BE EXTREMELY CONCISE. Aim for 1-2 sentences max.
        2. NO LISTS unless absolutely necessary.
        3. DIRECT ANSWER ONLY.
        4. STOP generating as soon as the answer is complete.
        5. NO MARKDOWN BOLD/ITALICS. Use double quotes (" ") for highlighting.
        
        NEGATIVE CONSTRAINTS (STRICT):
        - DO NOT add a "Skills" section unless the user asks for skills OR role fitness OR project details (mentioning tech stack is required for projects).
        - DO NOT list "Projects" unless the user asks for projects OR asks about role fitness. If asking about role fitness, you MUST mention relevant project names.
        - DO NOT repeat the answer in bullet points if you already wrote a sentence.
        - IF THE QUESTION IS ABOUT A DATE, PROVIDE THE DATE ONLY.
        """

        try:
            print(f"Generating response using model: llama-3.1-8b-instant w/ temp: 0.5")  # Log model usage
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
                model="llama-3.1-8b-instant", # Using the valid 8B model
                temperature=0.5,
                max_tokens=256,
            )
            # Log Token Usage
            usage = chat_completion.usage
            if usage:
                print(f"Token Usage -> Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, Total: {usage.total_tokens}")
            
            print("Response generated successfully.")  # Confirm success
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
