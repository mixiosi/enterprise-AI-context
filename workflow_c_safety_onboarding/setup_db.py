import sqlite3
import os

DB_PATH = "site_safety.db"

def setup_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Registered Personnel (People who already have orientation)
    c.execute('''CREATE TABLE site_roster (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    company TEXT,
                    last_orientation_date TEXT
                )''')
                
    # Insert existing people
    c.executemany("INSERT INTO site_roster (name, company, last_orientation_date) VALUES (?, ?, ?)", [
        ("Michael Scott", "Dunder Mifflin", "2024-05-12"),
        ("Dwight Schrute", "Dunder Mifflin", "2024-05-12"),
        ("Jim Halpert", "Dunder Mifflin", "2025-01-20")
    ])

    # 2. PPE Inventory
    c.execute('''CREATE TABLE ppe_inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_type TEXT,
                    size TEXT,
                    quantity INTEGER
                )''')
                
    # Insert inventory (Notice size 11 boots are out of stock)
    c.executemany("INSERT INTO ppe_inventory (item_type, size, quantity) VALUES (?, ?, ?)", [
        ("Hardhat", "One Size", 45),
        ("Safety Glasses", "One Size", 120),
        ("High-Vis Vest", "L", 30),
        ("High-Vis Vest", "XL", 15),
        ("Steel Toe Boots", "9", 5),
        ("Steel Toe Boots", "10", 8),
        ("Steel Toe Boots", "11", 0),  # Out of stock
        ("Steel Toe Boots", "12", 3)
    ])

    # 3. Orientation Schedule
    c.execute('''CREATE TABLE orientation_schedule (
                    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    slots_available INTEGER
                )''')
                
    # Insert upcoming classes
    c.executemany("INSERT INTO orientation_schedule (date, time, slots_available) VALUES (?, ?, ?)", [
        ("Tomorrow", "08:00 AM", 5),
        ("Next Tuesday", "08:00 AM", 10),
        ("Next Wednesday", "08:00 AM", 0)  # Full class
    ])

    conn.commit()
    conn.close()
    print("✅ site_safety.db successfully created and populated with mock data.")

if __name__ == "__main__":
    setup_database()
