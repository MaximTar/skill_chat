import json
import textwrap
from datetime import datetime

from flask import Flask, render_template, request

# Messages utils

test_msg = {'text': "Welcome to skill chat!",
            'sender': "Admin",
            'time': datetime.now().strftime("%H:%M")}

DB_FILE = "data/db.json"
MAX_MSG_LEN = 3000


def load_msgs():
    try:
        with open(DB_FILE, "r") as json_db:
            return json.load(json_db)["msgs"]
    except FileNotFoundError:
        with open(DB_FILE, "w+"):
            return []


msgs = load_msgs()


def save_msgs():
    with open(DB_FILE, "w") as json_db:
        json.dump({"msgs": msgs}, json_db)


def add_msg(text: str, sender: str):
    msgs.append({'text': text,
                 'sender': sender,
                 'time': datetime.now().strftime("%H:%M")})
    save_msgs()


# Useless code (day 1)
# def print_msg(msg: dict):
#     try:
#         print(f"[{msg['sender']}]: {msg['text']} / {msg['time']}")
#     except TypeError:
#         pass  # log
#     except KeyError:
#         pass  # log
#
#
# def print_all_msgs():
#     for msg in msgs:
#         print_msg(msg)


# Flask utils

app = Flask(__name__)


@app.route("/")
def main_page():
    return "Welcome to skill_chat main page!\nPlease move to /chat page."


@app.route("/all_msgs")
def all_msgs():
    return {"msgs": msgs}


@app.route("/send_msg")
def send_msg():
    text = request.args["text"]
    sender = request.args["sender"]

    if len(sender) < 3 or len(sender) > 100 or len(text) < 1:
        return {"status": "Error", "text": "Too short message or wrong name!"}

    elif len(text) > MAX_MSG_LEN:
        split_text = textwrap.wrap(text, MAX_MSG_LEN, break_long_words=False)

        if len(split_text[0]) > MAX_MSG_LEN:
            return {"status": "Error", "text": "Too long message!"}

        for new_text in split_text:
            add_msg(new_text, sender)
        return {"status": "Ok", "text": ""}

    else:
        add_msg(text, sender)
        return {"status": "Ok", "text": ""}


@app.route("/chat")
def display_chat():
    return render_template("form.html")


if __name__ == '__main__':
    app.run()
