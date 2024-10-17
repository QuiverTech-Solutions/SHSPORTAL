import sqlite3
from datetime import datetime, date

# Connection to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('shs_web.db')
cursor = conn.cursor()

# Create Users Table
def create_users_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role_id TEXT NOT NULL,
            school_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Insert data into users table
    cursor.executemany('''
        INSERT INTO users (user_id, first_name, last_name, email, hashed_password, role_id, school_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        ("f6fd6f26-fba5-4927-a2f5-dfdeb4248ca1", "Admin", "Admin", "superadmin@admin.com", "<hashed_password>",
         "790c09c4-f16c-42f8-8b37-1a35110dc4bf", None, datetime.now()),
        ("e4b9606a-bfcd-4ac6-afc1-37788ab2024f", "School", "Admin", "schooladmin@springfield.com", "<hashed_password>",
         "bcd1f3b8-5096-4920-bf6b-8becd6d714c3", "0f85a9b0-f3da-41e6-9b3b-9a0cdb29fbbb", datetime.now())
    ])
    conn.commit()

# Create Students Table
def create_students_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            index_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            dob DATE NOT NULL,
            school_id TEXT,
            location TEXT NOT NULL,
            registration_paid BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Insert data into students table
    cursor.executemany('''
        INSERT INTO students (id, index_number, name, dob, school_id, location, registration_paid, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        ("d6f8a1f4-8c7b-11ec-b909-0242ac120002", "10829279", "Kwame Mensah", date(2005, 4, 12),
         "0f85a9b0-f3da-41e6-9b3b-9a0cdb29fbbb", "Accra", True, datetime.now()),
        ("f4a1a6e8-8c7b-11ec-b909-0242ac120002", "10829274", "Ama Owusu", date(2006, 6, 22),
         "0f85a9b0-f3da-41e6-9b3b-9a0cdb29fbbb", "Accra", False, datetime.now()),
        ("d0e2bfa6-8c7b-11ec-b909-0242ac120002", "10829273", "Yaw Antwi", date(2004, 11, 10),
         "1f45c3a2-c1b8-4e19-9b5d-529b0a7187cb", "Kumasi", True, datetime.now()),
        ("e7ab82f0-8c7b-11ec-b909-0242ac120002", "10829272", "Esi Asante", date(2005, 8, 14),
         "1f45c3a2-c1b8-4e19-9b5d-529b0a7187cb", "Kumasi", False, datetime.now())
    ])
    conn.commit()

# Create Schools Table
def create_schools_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schools (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            registration_fee REAL DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Insert data into schools table
    cursor.executemany('''
        INSERT INTO schools (id, name, location, registration_fee, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ("0f85a9b0-f3da-41e6-9b3b-9a0cdb29fbbb", "Springfield High School", "Accra", 50.00, datetime.now()),
        ("1f45c3a2-c1b8-4e19-9b5d-529b0a7187cb", "Riverbank Academy", "Kumasi", 30.00, datetime.now())
    ])
    conn.commit()

# Create Roles Table
def create_roles_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Insert data into roles table
    cursor.executemany('''
        INSERT INTO roles (id, name)
        VALUES (?, ?)
    ''', [
        ("790c09c4-f16c-42f8-8b37-1a35110dc4bf", "super_admin"),
        ("bcd1f3b8-5096-4920-bf6b-8becd6d714c3", "school_admin")
    ])
    conn.commit()

# Call the functions to create tables and seed data
create_users_table()
create_students_table()
create_schools_table()
create_roles_table()

# Close connection when done
conn.close()
