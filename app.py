
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_agent import PortfolioAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes, allowing requests from any origin for development
CORS(app)

# Initialize the agent
try:
    agent = PortfolioAgent()
    print("Portfolio Agent initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Portfolio Agent: {e}")
    agent = None

@app.route('/api/chat', methods=['POST'])
def chat():
    if not agent:
        return jsonify({"error": "Agent not initialized. Check GROQ_API_KEY."}), 500
    
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    response = agent.get_response(user_message)
    return jsonify({"response": response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "agent_initialized": agent is not None})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
