from flask import Flask, render_template, Response, request, jsonify
import os
import time
import requests

app = Flask(__name__)

# Gemini (Google) API setup
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
)

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")


# Function to interact with Gemini API
def get_gemini_response(message):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": message}]}]}

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}", json=data, headers=headers
        )
        response.raise_for_status()
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with Gemini API: {e}")
        return "Sorry, I'm having trouble reaching the server."


# Simulated streaming response
def generate_streaming_response():
    messages = ["Hello! How can I assist you today?"]

    for msg in messages:
        yield f"data: {msg}\n\n"
        time.sleep(0.5)

    user_input = "Tell me a joke"
    gemini_response = get_gemini_response(user_input)
    yield f"data: {gemini_response}\n\n"

    more_response = get_gemini_response("Tell me another joke")
    yield f"data: {more_response}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(generate_streaming_response(), content_type="text/event-stream")


@app.route("/save_title", methods=["POST"])
def save_title():
    title = request.json.get("title")
    with open("conversation_titles.txt", "a") as f:
        f.write(title + "\n")
    return {"status": "success"}


@app.route("/clear", methods=["POST"])
def clear_conversation():
    try:
        open("conversation_titles.txt", "w").close()
        return {"status": "cleared"}
    except:
        return {"status": "error"}


if __name__ == "__main__":
    app.run(debug=True)