import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")


def get_nutrient(food, names):
    names = {name.lower() for name in names}

    for nutrient in food.get("foodNutrients", []):
        nutrient_name = nutrient.get(
            "nutrientName",
            ""
        ).lower()

        if nutrient_name in names:
            return nutrient.get("value", 0)

    return "N/A"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(silent=True) or {}
        food_name = data.get("food_name", "").strip()

        if not food_name:
            return jsonify({
                "error": "Please enter a food name"
            }), 400

        response = requests.post(
            "https://api.nal.usda.gov/fdc/v1/foods/search",
            params={
                "api_key": USDA_API_KEY
            },
            json={
                "query": food_name,
                "pageSize": 1
            },
            timeout=30
        )

        if not response.ok:
            return jsonify({
                "error": "Nutrition API request failed",
                "details": response.text
            }), response.status_code

        foods = response.json().get("foods", [])

        if not foods:
            return jsonify({
                "error": f"No nutrition data found for '{food_name}'"
            }), 404

        food = foods[0]

        return jsonify({
            "food": food.get("description", food_name),
            "calories": get_nutrient(food, ["energy"]),
            "protein": get_nutrient(food, ["protein"]),
            "carbs": get_nutrient(
                food,
                [
                    "carbohydrate, by difference",
                    "carbohydrates"
                ]
            ),
            "fat": get_nutrient(
                food,
                [
                    "total lipid (fat)",
                    "total fat"
                ]
            ),
            "fiber": get_nutrient(
                food,
                [
                    "fiber, total dietary",
                    "dietary fiber"
                ]
            )
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "The nutrition service took too long to respond"
        }), 504

    except requests.exceptions.RequestException as error:
        return jsonify({
            "error": f"Request failed: {str(error)}"
        }), 502

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True
    )