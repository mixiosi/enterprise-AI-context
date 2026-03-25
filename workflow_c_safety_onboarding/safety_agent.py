import sqlite3
import json
import time

DB_PATH = "site_safety.db"

# Simulated AI Extractor Function (to represent an LLM parsing the email)
def extract_email_data(email_body):
    """Simulates an LLM extracting entities from an unstructured email."""
    print(f"\n🧠 [AI Extraction Module] Scanning incoming email for site visit intent...")
    time.sleep(1.5)
    
    # We use simple keyword matching to mock the LLM's structured JSON output
    data = {"is_new_visitor": False, "name": None, "company": None, "date": None, "shoe_size": None}
    
    if "Mark Brendanawicz" in email_body:
        data = {
            "is_new_visitor": True,
            "name": "Mark Brendanawicz",
            "company": "Pawnee Contracting",
            "date": "Tomorrow",
            "shoe_size": None # Missing data!
        }
    elif "Ron Swanson" in email_body:
        data = {
            "is_new_visitor": True,
            "name": "Ron Swanson",
            "company": "Swanson Carpentry",
            "date": "Next Tuesday",
            "shoe_size": "11" # Out of stock in DB!
        }
    elif "April Ludgate" in email_body:
        data = {
            "is_new_visitor": True,
            "name": "April Ludgate",
            "company": "Pawnee Parks Dept",
            "date": "Next Tuesday",
            "shoe_size": "9"
        }
        
    print(f"✅ Extraction Complete: {json.dumps(data, indent=2)}")
    return data

# Database Interaction Tools
def check_if_registered(name):
    print(f"🔎 [Database Check] Searching site roster for '{name}'...")
    time.sleep(1)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM site_roster WHERE name=?", (name,))
    result = c.fetchone()
    conn.close()
    return result is not None

def book_orientation(date):
    print(f"📅 [Scheduling] Checking orientation class availability for '{date}'...")
    time.sleep(1)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT class_id, time, slots_available FROM orientation_schedule WHERE date=?", (date,))
    result = c.fetchone()
    
    if result and result[2] > 0:
        class_id, class_time, slots = result
        new_slots = slots - 1
        c.execute("UPDATE orientation_schedule SET slots_available=? WHERE class_id=?", (new_slots, class_id))
        conn.commit()
        conn.close()
        print(f"   ✅ Successfully booked slot for {date} at {class_time}. ({new_slots} slots remaining)")
        return True, class_time
    conn.close()
    print(f"   ❌ No available classes found for {date}.")
    return False, None

def check_ppe_inventory(shoe_size):
    print(f"👷 [Inventory Check] Verifying PPE stock levels...")
    time.sleep(1)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    status = []
    issues = []
    
    # Check standard items
    for item in ["Hardhat", "Safety Glasses", "High-Vis Vest"]:
        c.execute("SELECT quantity FROM ppe_inventory WHERE item_type=?", (item,))
        qty = sum([row[0] for row in c.fetchall()])
        if qty > 0:
            status.append(f"{item} (In Stock)")
        else:
            issues.append(f"{item} (OUT OF STOCK)")
            
    # Check specific shoe size
    if shoe_size:
        c.execute("SELECT quantity FROM ppe_inventory WHERE item_type='Steel Toe Boots' AND size=?", (shoe_size,))
        row = c.fetchone()
        if row and row[0] > 0:
            status.append(f"Steel Toe Boots Size {shoe_size} (In Stock)")
        else:
            issues.append(f"Steel Toe Boots Size {shoe_size} (OUT OF STOCK)")
    else:
        issues.append("Steel Toe Boots (SIZE UNKNOWN)")
        
    conn.close()
    return status, issues

# Main Agent Workflow
def process_email(email_body):
    print("\n" + "="*60)
    print("📨 NEW EMAIL DETECTED IN INBOX:")
    print(f"\"{email_body}\"")
    print("="*60)
    
    # 1. Extract context
    data = extract_email_data(email_body)
    
    if not data["is_new_visitor"]:
        print("⏭️ No new visitor detected. Archiving email.")
        return
        
    name = data["name"]
    date = data["date"]
    shoe_size = data["shoe_size"]
    company = data["company"]
    
    # 2. Check if already registered
    if check_if_registered(name):
        print(f"✅ {name} is already registered on site. No orientation needed.")
        return
        
    print(f"⚠️ {name} is a NEW VISITOR. Initiating onboarding workflow...")
    
    # 3. Book orientation
    booked, class_time = book_orientation(date)
    orientation_status = f"Booked for {date} at {class_time}" if booked else f"ACTION REQUIRED: Could not book class for {date}"
    
    # 4. Check PPE
    stock_status, stock_issues = check_ppe_inventory(shoe_size)
    
    # 5. Draft Email to Safety Manager
    print(f"\n📤 [Communication] Generating heads-up email to Safety Manager...")
    time.sleep(1.5)
    
    email_draft = f"""
SUBJECT: NEW VISITOR ALERT: {name} ({company}) arriving {date}
TO: Safety Manager
---------------------------------------------------------
Hello,

The AI Assistant has detected that a new person, {name} from {company}, is scheduled to arrive on site {date}. 

📅 ORIENTATION STATUS:
{orientation_status}

👷 PPE INVENTORY STATUS:
Available: {', '.join(stock_status) if stock_status else 'None'}
Action Needed: {', '.join(stock_issues) if stock_issues else 'None'}
"""
    
    # 6. Exception Handling / Assistant drafting
    if "Steel Toe Boots (SIZE UNKNOWN)" in stock_issues:
        email_draft += f"\n⚠️ NOTE: We do not have their shoe size on file. I have drafted an email for you to send to {name} requesting their boot size so we can verify inventory before they arrive."
    elif any("OUT OF STOCK" in issue for issue in stock_issues):
        email_draft += f"\n⚠️ URGENT: We are out of stock for some required PPE items. Please place an order immediately."
        
    email_draft += "\nBest,\nYour Enterprise AI Automations"
    print(email_draft)
    print("="*60)


if __name__ == "__main__":
    # Test Scenario 1: The Perfect Run
    email1 = "Hey everyone, April Ludgate from the Pawnee Parks Dept will be visiting the site Next Tuesday to observe the dig. She wears a size 9 boot."
    
    # Test Scenario 2: Missing Information
    email2 = "Hi, Mark Brendanawicz (Pawnee Contracting) is doing a walkthrough Tomorrow."
    
    # Test Scenario 3: Inventory Issue
    email3 = "Just confirming Ron Swanson (Swanson Carpentry) is arriving Next Tuesday. He needs a size 11 boot."
    
    print("\n🚀 STARTING SAFETY ONBOARDING AUTOMATION WORKFLOW...")
    
    process_email(email1)
    time.sleep(3)
    process_email(email2)
    time.sleep(3)
    process_email(email3)

