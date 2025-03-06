from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
genai.configure(api_key="AIzaSyDGN5p2ZGBDakNfd6GkBGFt8jrN_IVdl-0")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_health_assistance", methods=["POST"])
def get_health_assistance():
    try:
        user_data = request.get_json()
        symptoms = user_data['symptoms']
        
        # Enhanced prompt to include detailed information for each disease
        prompt = f"""  
        Given the symptoms: {symptoms}, predict possible diseases. For each disease, provide:
        - A brief description
        - Additional symptoms
        - Precautions
        - Suggested medications
        - Recommended workouts
        - Suitable diets
        - Expected outcomes
        """

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"healthAdvice": response.text})
        else:
            return jsonify({"error": "No advice generated"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

