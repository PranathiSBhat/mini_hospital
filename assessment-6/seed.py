import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mini_hospital'
)
cursor = conn.cursor()

# Clear old data
cursor.execute("DELETE FROM appointments")
cursor.execute("DELETE FROM patients")
cursor.execute("DELETE FROM doctors")

# Insert sample doctors
cursor.execute("INSERT INTO doctors (name, department) VALUES ('Dr. Alice', 'Cardiology')")
cursor.execute("INSERT INTO doctors (name, department) VALUES ('Dr. Bob', 'Neurology')")

conn.commit()
conn.close()

print("Seed complete.")
