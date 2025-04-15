from flask import Flask, request, jsonify
from transformers import pipeline
import re

app = Flask(__name__)

# Load lightweight chatbot model
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

# Crisis detection keywords
crisis_keywords = [
    r"\bhopeless\b", r"\bsuicide\b", r"\bworthless\b", r"\bno point\b",
    r"\bend it all\b", r"\bkill myself\b", r"\bcant go on\b"
]

# Game data and story scenes
game_state = {
    "player": {
        "name": "",
        "mood": "neutral",
        "meds": [],
        "inventory": []
    },
    "scene": "colony_outskirts",
    "quests": ["find_supplies", "help_stranger"],
    "choices": {},
    "progress": 0
}

story = {
    "colony_outskirts": {
        "text": "You stand on the dusty outskirts of a sci-fi colony. A crate of supplies glints nearby, but a weary stranger watches you. Do you: 1) Open the crate, 2) Talk to the stranger, 3) Rest and reflect?",
        "options": ["open", "talk", "rest"],
        "next_scenes": {
            "open": "colony_crate",
            "talk": "colony_stranger",
            "rest": "colony_outskirts"
        }
    },
    "colony_crate": {
        "text": "You open the crate, finding a medkit and a journal. The stranger frowns, saying it’s theirs. Do you: 1) Give it back, 2) Keep it, 3) Share the supplies?",
        "options": ["give", "keep", "share"],
        "next_scenes": {
            "give": "colony_end",
            "keep": "colony_end",
            "share": "colony_end"
        }
    },
    "colony_stranger": {
        "text": "The stranger shares their story of loss. They ask for help finding water. Do you: 1) Offer your canteen, 2) Search together, 3) Wish them luck?",
        "options": ["offer", "search", "wish"],
        "next_scenes": {
            "offer": "colony_end",
            "search": "colony_end",
            "wish": "colony_end"
        }
    },
    "colony_end": {
        "text": "The colony hums with life. Your actions shaped its future. Want to reflect on your journey or start anew?",
        "options": ["reflect", "restart"],
        "next_scenes": {
            "reflect": "colony_outskirts",
            "restart": "colony_outskirts"
        }
    }
}

resources = {
    "audiobooks": [
        {"title": "As a Man Thinketh", "url": "https://archive.org/download/as_a_man_thinketh_librivox/as_a_man_thinketh_01_allen.mp3"},
        {"title": "The Power of Concentration", "url": "https://archive.org/download/power_concentration_1006_librivox/powerofconcentration_01_dumont.mp3"}
    ],
    "songs": [
        {"title": "Calm Ambient 432Hz", "url": "https://freemusicarchive.org/music/Scott_Holmes/Inspiring_Background_Music/Scott_Holmes_-_Calm_and_Ambient.mp3"},
        {"title": "Serenity", "url": "https://freemusicarchive.org/music/Kai_Engel/Satin/Kai_Engel_-_Satin_-_05_Serenity.mp3"}
    ],
    "coping_slides": [
        {"text": "Box Breathing: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s.", "image": "https://via.placeholder.com/300x200.png?text=Box+Breathing"},
        {"text": "5-4-3-2-1 Grounding: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.", "image": "https://via.placeholder.com/300x200.png?text=Grounding"},
        {"text": "Gratitude Journal: Write 3 things you’re thankful for today.", "image": "https://via.placeholder.com/300x200.png?text=Gratitude"},
        {"text": "Progressive Muscle Relaxation: Tense and release each muscle group.", "image": "https://via.placeholder.com/300x200.png?text=Relaxation"},
        {"text": "Positive Affirmation: Repeat 'I am enough.'", "image": "https://via.placeholder.com/300x200.png?text=Affirmation"}
    ]
}

@app.route("/start", methods=["POST"])
def start_game():
    game_state["player"]["name"] = request.json.get("name", "Colonist")
    game_state["scene"] = "colony_outskirts"
    game_state["choices"] = {}
    game_state["progress"] = 0
    return jsonify({
        "scene": game_state["scene"],
        "text": story[game_state["scene"]]["text"],
        "options": story[game_state["scene"]]["options"],
        "resources": resources,
        "message": f"Welcome, {game_state['player']['name']}! Your journey begins."
    })

@app.route("/choose", methods=["POST"])
def make_choice():
    choice = request.json.get("choice")
    scene = game_state["scene"]
    if choice in story[scene]["options"]:
        game_state["choices"][scene] = choice
        game_state["progress"] += 1
        next_scene = story[scene]["next_scenes"].get(choice, "colony_outskirts")
        game_state["scene"] = next_scene
        if scene == "colony_crate" and choice in ["keep", "share"]:
            game_state["player"]["inventory"].append("medkit")
        if choice == "rest":
            return jsonify({
                "text": story[next_scene]["text"],
                "options": story[next_scene]["options"],
                "therapy": "Resting’s wise. Try this: Breathe deeply for 10 seconds. How do you feel?"
            })
        return jsonify({
            "text": story[next_scene]["text"],
            "options": story[next_scene]["options"]
        })
    return jsonify({"error": "Invalid choice"}, 400)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    for keyword in crisis_keywords:
        if re.search(keyword, user_input.lower()):
            return jsonify({
                "reply": "I hear you’re struggling. You’re not alone. Want to try a coping strategy or call the lifeline?",
                "lifeline": True,
                "suggestion": resources["coping_slides"][0]
            })
    if "reflect" in game_state["choices"].values() or "rest" in game_state["choices"].values():
        return jsonify({
            "reply": "Reflecting’s powerful. Try naming one thing you’re proud of today.",
            "exercise": "gratitude"
        })
    try:
        response = chatbot(user_input)
        reply = response[-1]["generated_text"]
    except Exception:
        reply = "I’m listening—tell me more."
    return jsonify({"reply": reply})

@app.route("/meds", methods=["POST"])
def add_med():
    med = request.json.get("med")
    if med:
        game_state["player"]["meds"].append({"name": med, "reminder": "daily"})
        return jsonify({"message": f"Added {med}. You’ll get a daily reminder."})
    return jsonify({"error": "Missing med name"}, 400)

@app.route("/meds", methods=["GET"])
def get_meds():
    return jsonify({"meds": game_state["player"]["meds"]})

@app.route("/lifeline", methods=["GET"])
def lifeline():
    return jsonify({
        "message": "Connecting to crisis support (e.g., 988). You’re not alone.",
        "hotline": "tel:+1-800-273-8255"
    })

@app.route("/resources", methods=["GET"])
def get_resources():
    return jsonify(resources)

if __name__ == "__main__":
    app.run(debug=True)

# --- Additional Routes ---


# Mock data storage
appointments = [
    {"date": "2025-04-25", "time": "9:00 AM", "type": "Therapy"},
    {"date": "2025-04-29", "time": "11:30 AM", "type": "Therapy"},
    {"date": "2025-05-03", "time": "2:00 PM", "type": "Zoom Movie Night"},
    {"date": "2025-05-06", "time": "10:00 AM", "type": "Open Mic"}
]

guardian_profile = {
    "vitals": "135/88 mmHg",
    "medication": [
        {"name": "Aripiprazole", "dose": "15 mg"},
        {"name": "Clonazepam", "dose": "1 mg"},
        {"name": "Lithium", "dose": "900 mg"}
    ],
    "hospital": "Greenwood Psychiatric"
}

event_schedule = {
    "topic": "Movie Night / Open Mic",
    "time": "8:00 PM",
    "hospital": "Greenwood Psychiatric",
    "link": "https://zoom.us/j/0000000000"
}

@app.route("/appointments", methods=["GET", "POST"])
def manage_appointments():
    if request.method == "GET":
        return jsonify(appointments)
    if request.method == "POST":
        data = request.json
        if "date" in data and "time" in data and "type" in data:
            appointments.append(data)
            return jsonify({"message": "Appointment added", "appointments": appointments})
        return jsonify({"error": "Missing fields"}), 400

@app.route("/guardian", methods=["GET"])
def get_guardian_profile():
    return jsonify(guardian_profile)

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(event_schedule)