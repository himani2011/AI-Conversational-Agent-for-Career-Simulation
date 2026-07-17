from database.db import init_db, save_chat, get_chats
from flask import Flask, request, jsonify
from chatbot.career_agent import ask_career_bot

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return "AI Career Coach API is running!"

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Please provide a message"}), 400

    user_message = data["message"]

    bot_response = ask_career_bot(user_message)

    # Save to DB
    save_chat(user_message, bot_response)

    return jsonify({
        "user_message": user_message,
        "bot_response": bot_response
    })

@app.route("/history", methods=["GET"])
def history():
    chats = get_chats()

    return jsonify({
        "chat_history": chats
    })

if __name__ == "__main__":
    app.run(debug=True)