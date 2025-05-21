from flask import Flask, render_template, request, jsonify
import pyrebase

app = Flask(__name__)

firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

booking_state = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.json["msg"].lower()
    user_id = request.json.get("user_id", "default")  # You can use user sessions later
    
    if user_id not in booking_state:
        booking_state[user_id] = {}

    state = booking_state[user_id]

    if "table" in user_msg or "available" in user_msg:
        tables = db.child("tables").get().val()
        reply = ""
        for key, table in tables.items():
            reply += f"Table {table['table_id']} has {table['seats']} seats. Available at: {', '.join(table['available_times'])}\n"
        return jsonify({"reply": reply.strip()})

    elif "book" in user_msg:
        state.clear()
        state['step'] = 'name'
        return jsonify({"reply": "Sure! What is your name?"})

    elif 'step' in state:
        if state['step'] == 'name':
            state['name'] = user_msg
            state['step'] = 'people'
            return jsonify({"reply": "Got it! How many people will be joining?"})
        elif state['step'] == 'people':
            state['people'] = user_msg
            state['step'] = 'time'
            return jsonify({"reply": "Thanks! What time would you like to reserve?"})
        elif state['step'] == 'time':
            state['time'] = user_msg
            # Save reservation in Firebase
            reservation = {
                "name": state['name'],
                "people": state['people'],
                "time": state['time']
            }
            db.child("reservations").push(reservation)
            booking_state.pop(user_id)  # Clear after done
            return jsonify({"reply": "Your reservation is confirmed! Thank you."})

    else:
        return jsonify({"reply": "Sorry, I didn't understand. You can ask about table availability or make a reservation."})

if __name__ == "__main__":
    app.run(debug=True)
