import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBIwzk8UjzzGCuog6LZvBHcPkZyzjXjtgQ",
  "authDomain": "restaurant-chatbot-e6f7d.firebaseapp.com",
  "databaseURL": "https://restaurant-chatbot-e6f7d-default-rtdb.firebaseio.com",
  "storageBucket": "restaurant-chatbot-e6f7d.firebasestorage.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

data = db.get()
print("Top-level keys in your database:")
for item in data.each():
    print(item.key())
