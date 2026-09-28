from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "database/chat.db"


# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_chats():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    chats = conn.execute("""
        SELECT * FROM chats
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return chats


# ---------------- CHATBOT ----------------

def chatbot_response(message):

    message = message.lower().strip()

    if any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! 👋 Welcome to our customer support. How can I help you?"

    elif "price" in message or "pricing" in message:
        return "Our pricing depends on the selected product or service. Please provide the product name."

    elif "order" in message and "status" in message:
        return "Please provide your order ID so we can help you check the order status."

    elif "delivery" in message or "shipping" in message:
        return "Standard delivery usually takes a few business days. Delivery time may vary depending on the location."

    elif "refund" in message:
        return "For refund-related requests, please provide your order ID and reason for the refund."

    elif "payment" in message:
        return "We support common online payment methods. If your payment failed, please check your payment details and try again."

    elif "password" in message:
        return "If you forgot your password, use the password reset option on the login page."

    elif "account" in message:
        return "I can help with basic account-related questions. Please tell me what you need help with."

    elif "thank" in message:
        return "You're welcome! 😊 I'm happy to help."

    elif "bye" in message:
        return "Goodbye! 👋 Have a great day."

    else:
        return (
            "I'm not sure about that yet. "
            "Please try asking about orders, delivery, payments, refunds, "
            "passwords, pricing, or accounts."
        )


# ---------------- HOME ----------------

@app.route("/")
def home():

    chats = get_chats()

    return render_template(
        "index.html",
        chats=chats
    )


# ---------------- SEND MESSAGE ----------------

@app.route("/chat", methods=["POST"])
def chat():

    message = request.form.get("message")

    if message:

        response = chatbot_response(message)

        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO chats
            (user_message, bot_response, created_at)
            VALUES (?, ?, ?)
        """, (
            message,
            response,
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


# ---------------- CLEAR CHAT ----------------

@app.route("/clear")
def clear_chat():

    conn = sqlite3.connect(DATABASE)

    conn.execute("DELETE FROM chats")

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# ---------------- RUN ----------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)