from flask import Flask, request, render_template, jsonify
import mysql.connector
from datetime import datetime, time as time_obj

app = Flask(__name__)

# DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mini_hospital'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('index.html', doctors=doctors, message=None)

@app.route('/doctors', methods=['GET'])
def get_doctors():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/patients', methods=['GET'])
def get_patients():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/appointments', methods=['GET'])
def get_appointments():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    time_str = request.form['time']

    # Validate time
    try:
        appt_time = datetime.strptime(time_str, "%H:%M").time()
        if appt_time < time_obj(9, 0) or appt_time >= time_obj(17, 0):
            raise ValueError("Time outside clinic hours")
    except ValueError:
        return render_with_message("Invalid time. Clinic hours: 09:00–17:00.")

    conn = get_db()
    cursor = conn.cursor()

    # Insert patient
    cursor.execute("INSERT INTO patients (name, phone) VALUES (%s, %s)", (name, phone))
    patient_id = cursor.lastrowid

    # Check appointment conflict
    cursor.execute("""
        SELECT * FROM appointments
        WHERE doctor_id = %s AND date = %s AND time = %s
    """, (doctor_id, date, time_str))
    if cursor.fetchone():
        conn.close()
        return render_with_message("Error: Doctor already has an appointment at that time.")

    # Insert appointment
    cursor.execute("""
        INSERT INTO appointments (doctor_id, patient_id, date, time)
        VALUES (%s, %s, %s, %s)
    """, (doctor_id, patient_id, date, time_str))
    conn.commit()
    conn.close()

    return render_with_message("✅ Appointment booked successfully!")

def render_with_message(message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('index.html', doctors=doctors, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


