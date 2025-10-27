
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

def get_db_connection():
    conn = sqlite3.connect('donation_management.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    total_donations = conn.execute('SELECT SUM(donation_amount) FROM donation_records').fetchone()[0]
    donation_count = conn.execute('SELECT COUNT(*) FROM donation_records').fetchone()[0]
    donor_count = conn.execute('SELECT COUNT(*) FROM donor_store_profiles').fetchone()[0]
    conn.close()
    return render_template('index.html', total_donations=total_donations, donation_count=donation_count, donor_count=donor_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # You should hash and verify this
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and password == user['password_hash']:  # Replace with proper hash check
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            if user['role'] == 'donor':
                return redirect('/donor-dashboard')
            else:
                return redirect('/npo-dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Hash this before storing
        role = request.form['role']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
                     (name, email, password, role))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/donor-dashboard')
def donor_dashboard():
    return render_template('donor-dashboard.html')

@app.route('/npo-dashboard')
def npo_dashboard():
    return render_template('npo-dashboard.html')

@app.route('/schedule-pickup', methods=['GET', 'POST'])
def schedule_pickup():
    if request.method == 'POST':
        donor_id = session.get('user_id')
        date = request.form['scheduled_date']
        address = request.form['pickup_address']
        contact = request.form['contact_person']
        phone = request.form['contact_phone']
        conn = get_db_connection()
        conn.execute('INSERT INTO pickup_scheduling (donor_store_id, scheduled_date, pickup_address, contact_person, contact_phone) VALUES (?, ?, ?, ?, ?)',
                     (donor_id, date, address, contact, phone))
        conn.commit()
        conn.close()
        return redirect('/donor-dashboard')
    return render_template('schedule-pickup.html')

if __name__ == '__main__':
    app.run(debug=True)
