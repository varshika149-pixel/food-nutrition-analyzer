# Food Nutrition Analyzer

A simple web application that allows users to enter a food name and view its estimated nutritional values.

## Features

- Search for food by name.
- Display calories.
- Display protein.
- Display carbohydrates.
- Display fat.
- Display dietary fiber.
- Simple and responsive user interface.
- Uses Flask for the backend.
- Uses USDA FoodData Central for nutrition data.

## Technologies Used

- HTML
- CSS
- JavaScript
- Python
- Flask
- Flask-CORS
- Requests
- USDA FoodData Central API

## How to Run

Install the required packages:
```bash
pip install flask flask-cors requests python-dotenv
```
Create a `.env` file:

```env
USDA_API_KEY=your_usda_api_key
```
Start the Flask server:
```bash
python app.py
```

Open `index.html` in a browser or serve it through a local HTTP server.

## Note

The nutritional values are estimates and may vary depending on the food type, serving size, and preparation method.
