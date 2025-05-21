from flask import Flask, render_template, request, jsonify
import pyrebase

app = Flask(__name__)

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyBIwzk8UjzzGCuog6LZvBHcPkZyzjXjtgQ",
    "authDomain": "restaurant-chatbot-e6f7d.firebaseapp.com",
    "databaseURL": "https://restaurant-chatbot-e6f7d-default-rtdb.firebaseio.com",
    "projectId": "restaurant-chatbot-e6f7d",
    "storageBucket": "restaurant-chatbot-e6f7d.appspot.com",
    "messagingSenderId": "250604196892",
    "appId": "1:250604196892:web:d630b61a6a24a858053bd9"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.json["msg"].lower()

    # Simple logic: check for available tables
    if "table" in user_msg or "available" in user_msg:
        tables = db.child("tables").get().val()
        reply = ""
        for table in tables:
            reply += f"Table {table['table_id']} has {table['seats']} seats. Available at: {', '.join(table['available_times'])}\n"
        return jsonify({"reply": reply.strip()})
    
    elif "book" in user_msg:
        return jsonify({"reply": "Sure! Please tell me the time and number of people for the reservation."})
    
    else:
        return jsonify({"reply": "Sorry, I didn't understand. You can ask about table availability or make a reservation."})

if __name__ == "__main__":
    app.run(debug=True)
