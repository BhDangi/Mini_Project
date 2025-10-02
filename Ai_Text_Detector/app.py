from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Backend-only API key and model URL
API_KEY = "AIzaSyA1E7ET4oVOCymo_l1J64UMLoI_fJmAwPk"
MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY
            }
            # Prompt instructs Gemini to classify the text
            prompt = f"""
            You are an AI text detector. Determine if the following text is written by a human or AI.
            Answer only "Human-written" or "AI-generated".

            Text:
            \"\"\"{text}\"\"\"
            """
            data = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }
            try:
                response = requests.post(MODEL_URL, headers=headers, json=data)
                if response.status_code == 200:
                    response_json = response.json()
                    candidates = response_json.get("candidates", [])
                    if candidates:
                        result = candidates[0]["content"]["parts"][0]["text"]
                    else:
                        result = "No content returned."
                else:
                    result = f"Error {response.status_code}: {response.text}"
            except Exception as e:
                result = f"Request error: {str(e)}"
        else:
            result = "Please enter some text."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
