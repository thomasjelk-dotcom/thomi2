from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# --- Domänenmodell ---
class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User(name='{self.name}')"

class Message:
    def __init__(self, content, sender, timestamp):
        self.content = content
        self.sender = sender  # Referenz auf User-Objekt
        self.timestamp = timestamp

class Classroom:
    def __init__(self, name):
        self.name = name
        self.participants = []  # Liste von User-Objekten
        self.messages = []     # Liste von Message-Objekten

    def add_participant(self, user):
        if user not in self.participants:
            self.participants.append(user)

    def add_message(self, content, sender):
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = Message(content, sender, timestamp)
        self.messages.append(message)
        self.add_participant(sender)  # Füge Sender hinzu, falls noch nicht vorhanden

# --- Ein Klassenraum für das MVP ---
classroom = Classroom("Mathe 101")

# --- Flask-Routen ---
@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")
        if name and content:
            # Prüfe, ob der Nutzer bereits existiert
            user = next((u for u in classroom.participants if u.name == name), None)
            if not user:
                user = User(name)
            classroom.add_message(content, user)
    return render_template("index.html", classroom=classroom)

if __name__ == "__main__":
    app.run(debug=True)
