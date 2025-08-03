from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('basha_bodol.db')
    cursor = conn.cursor()
    # Create a table to store quote requests
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        details TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# --- API Endpoints ---

@app.route('/')
def index():
    # This will render your HTML file
    return render_template('index.html')

@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    details = data.get('details')

    if not name or not email or not phone:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    try:
        conn = sqlite3.connect('basha_bodol.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (name, email, phone, details) VALUES (?, ?, ?, ?)",
                       (name, email, phone, details))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Database error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
