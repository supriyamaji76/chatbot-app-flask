from flask import Flask, request, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.form["message"]
        try:
            response = model.generate_content(user_input)
            response_text = response.text
        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render_template("index.html", user_input=user_input, response=response_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)