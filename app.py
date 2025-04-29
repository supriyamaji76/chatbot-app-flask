from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load your Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Flash 2.0 model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please send a message."}), 400

    try:
        response = model.generate_content(user_input)
        bot_message = response.text
    except Exception as e:
        bot_message = f"Error: {str(e)}"

    return jsonify({"response": bot_message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
