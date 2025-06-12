from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Kezdeti egyenleg és bank tőke
balance = 100  # Játékos egyenlege
bank_balance = 1000  # Bank tőkéje
purchases = 0  # Pörgetések száma

# Szimbólumok és azok nyereményei
symbols = ["triangle", "circle", "square", "star", "joker"]
prizes = {
    "triangle": 10,
    "circle": 20,
    "square": 40,
    "star": 100,
    "joker": 1000
}

# Szimbólumok előfordulásának valószínűsége
probabilities = {
    "triangle": 0.2,
    "circle": 0.13,
    "square": 0.1,
    "star": 0.09,
    "joker": 0.01
}

def spin():
    """Egy új pörgetést végez, és visszaadja a három szimbólumot."""
    return random.choices(symbols, weights=[probabilities[symbol] for symbol in symbols], k=3)

@app.route('/')
def index():
    """A főoldal renderelése, ahol a szlotta játék elérhető."""
    return render_template('index.html', bank_balance=bank_balance, balance=balance, game_over=balance <= 0)

@app.route('/play', methods=['POST'])
def play():
    global balance, bank_balance, purchases
    if balance < 2:
        return jsonify({"error": "Not enough money to play."}), 400

    purchases += 1
    balance -= 2  # A játék költsége
    bank_balance += 2  # A bank pénzének növelése

    result = spin()
    reward = 0
    
    if result[0] == result[1] == result[2]:
        reward = prizes[result[0]]
        balance += reward  # Nyertes összeg hozzáadása a játékos egyenlegéhez
        bank_balance -= reward  # A bank pénzének csökkentése

    # Ha a játékos pénze elfogyott
    if balance <= 0:
        balance = 0  # Az egyenleg nulla, vége a játéknak

    return jsonify({
        "result": result,
        "reward": reward,
        "balance": balance,
        "bank_balance": bank_balance,
        "game_over": balance <= 0  # Ha elfogyott a pénz, vége a játéknak
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
