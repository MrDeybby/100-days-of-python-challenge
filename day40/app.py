from flask import Flask, jsonify, request



app = Flask(__name__)
data = {
    "new york": {"temperature": 22, "description": "Cloudy"},
    "los angeles": {"temperature": 28, "description": "Sunny"},
    "chicago": {"temperature": 18, "description": "Rainy"},
    "miami": {"temperature": 30, "description": "Sunny"},
    "seattle": {"temperature": 15, "description": "Rainy"},
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Wheater API!"})

@app.route("/weather", methods=["GET"])
def get_all_weather():
    return jsonify(data)    

@app.route("/weather/<city>", methods=["GET"])
def get_weather_by_city(city):
    city = city.strip().lower()

    if not city in data:
        return jsonify({"error": "City not found."}), 404
    
    # Simulate weather data for demonstration
    weather_data = {
        "city": city,
        "temperature": data[city]["temperature"],
        "description": data[city]["description"]
    }
    
    return jsonify(weather_data), 200

@app.route("/weather", methods=["POST"])
def add_weather_data():
    json = request.json
    city = json.get("city", "").strip().lower()
    temperature = json.get("temperature")
    description = json.get("description")

    if not city or not temperature or not description:
        return jsonify({"error": "City, temperature, and description are required."}), 400
    
    if city in data:
        return jsonify({"error": "City already exists."}), 400
    
    data[city] = {"temperature": temperature, "description": description}
    return jsonify({"message": f"Weather data for {city} added successfully."}), 201

if __name__ == "__main__":
    app.run(debug=True)