from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 Use a valid API key
GENAI_API_KEY = "AIzaSyBJrtzyvIwJuaocQCs_1FpTuotL738JvMo"
genai.configure(api_key=GENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_health_assistance", methods=["POST"])
def get_health_assistance():
    try:
        user_data = request.get_json()
        symptoms = user_data.get("symptoms", "").strip()

        if not symptoms:
            return jsonify({"error": "Please enter symptoms."}), 400

        prompt = f"""
        Given the symptoms: {symptoms}, predict possible diseases.
        For each disease, provide:
        - A brief description
        - Additional symptoms
        - Precautions
        - Suggested medications
        - Recommended workouts
        - Suitable diets
        - Expected outcomes.
        """

        # 🔄 Use "gemini-1.5-flash" if "gemini-pro" is unavailable
        model = genai.GenerativeModel("gemini-1.5-flash")  # Free-tier model
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return jsonify({"healthAdvice": response.text})
        else:
            return jsonify({"error": "No advice generated. Try again."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
