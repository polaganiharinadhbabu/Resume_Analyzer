import os
import pymysql

# Connect to the MySQL server and specify the database
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise RuntimeError("DB_PASSWORD environment variable is not configured.")

connection = pymysql.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="joins",
)
cursor = connection.cursor()
try:
    cursor.execute("SELECT * FROM teacher")
    teacher = cursor.fetchall()
    print("Teacher:", teacher)

    cursor.execute("SELECT * FROM professor")
    professor = cursor.fetchall()
    print("professor:", professor)
finally:
    connection.close()
