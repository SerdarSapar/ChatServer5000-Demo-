from flask import Flask, request, render_template  # Connect Flask
from datetime import datetime
import json

# json.load - load data from a file
# json.dump - save data to a file

app = Flask(__name__)

MESSAGES_FILENAME = "messages_file.json"  # Name of the message file


# Loads messages from a file
def load_messages():
    # 1. File opened
    with open(MESSAGES_FILENAME, "r") as message_file:
        # 2. Read the data structure from the file
        data = json.load(message_file)
        # 3. Take messages from the structure
        return  data["messages"]



all_messages = load_messages()  # List of all messages


# Save all messages to a file
def save_messages():
    # 1. Open the file
    with open(MESSAGES_FILENAME, "w") as message_file:
        # 2. Prepare the data structure
        data = {
            "messages": all_messages
        }
        # 3. Write the data structure to a file
        json.dump(data, message_file)


# The function of adding a new message
# Example: add_message("Vasya", "Leave me a beer plz")
def add_message(sender, text):
    # <= begins with indentation code inside the function of this
    # Create a new message (new structure - dictionary)
    new_message = {
        "text": text,
        "sender": sender,
        "time": datetime.now().strftime("%H:%M"),  # "watch:minutes"
    }
    # Add a message to the list
    all_messages.append(new_message)
    save_messages()


# All messages output function
def print_all():
    for msg in all_messages:
        print(f'[{msg["sender"]}]: {msg["text"]} / {msg["time"]}')


# Example of calling a function without parameters
print_all()


@app.route("/")
def main_page():
    return "Hello, welcome to ChatServer5000"


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@app.route("/send_message")
def send_message():
    text = request.args["text"]
    name = request.args["name"]
    add_message(name, text)
    return "ok"


@app.route("/chat")
def chat():
    return render_template("form.html")  # Displaying the visual interface from a file form.html


# Adding a message
# UI: fields for entering the name and text and the "send" button

app.run(host="0.0.0.0", port=80)
