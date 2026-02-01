import json
import subprocess
import sys
import os

HEXES_FILE = "../data/hexes.json"
SESSION_FILE = "session.json"
PROBLEM_ID = "hello_world"

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

print("🌌 Galaxy Battle Client")
print("-----------------------")

# ---------- LOGIN ----------
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
        session = json.load(f)
    print(f"Logged in as {session['username']} (Team {session['team']})")
else:
    username = input("Discord username: ").strip()
    team = input("Choose team (red/blue): ").strip().lower()

    if team not in ["red", "blue"]:
        print("❌ Invalid team")
        sys.exit(1)

    session = {"username": username, "team": team}

    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2)

    print(f"✅ Logged in as {username} (Team {team})")

print("-----------------------")

# ---------- CHOOSE HEX ----------
try:
    hex_id = int(input("Enter Hex ID to attack: "))
except ValueError:
    print("❌ Hex ID must be a number")
    sys.exit(1)

with open(HEXES_FILE, "r") as f:
    hexes = json.load(f)

hex_tile = next((h for h in hexes if h["id"] == hex_id), None)

if not hex_tile:
    print("❌ Hex not found")
    sys.exit(1)

print(f"\nAttacking Hex {hex_id}")
print("Current owner:", hex_tile["owner"])
print("Difficulty:", hex_tile["difficulty"])

# ---------- LOAD PROBLEM ----------
with open(f"problems/{PROBLEM_ID}.json", "r") as f:
    problem = json.load(f)

with open(f"tests/{PROBLEM_ID}_test.json", "r") as f:
    test = json.load(f)

print("\nProblem:", problem["title"])
print(problem["description"])
input("\nPress ENTER to run tests...")

# ---------- RUN SOLUTION ----------
try:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        capture_output=True,
        text=True,
        timeout=5
    )
except Exception as e:
    print("❌ Runtime error:", e)
    sys.exit(1)

stdout = result.stdout.strip()
expected = test["expected_stdout"].strip()

# ---------- JUDGE ----------
print("\n-----------------------")

if stdout != expected:
    print("❌ FAIL")
    print("Expected:", repr(expected))
    print("Got     :", repr(stdout))
    sys.exit(0)

print("✅ PASS")

# ---------- CAPTURE LOGIC ----------
previous_owner = hex_tile["owner"]

# Update owner
hex_tile["owner"] = session["team"]

# Increase difficulty safely
current_diff = hex_tile["difficulty"]
if current_diff in DIFFICULTY_ORDER:
    idx = DIFFICULTY_ORDER.index(current_diff)
    if idx < len(DIFFICULTY_ORDER) - 1:
        hex_tile["difficulty"] = DIFFICULTY_ORDER[idx + 1]

# Save back to JSON
with open(HEXES_FILE, "w") as f:
    json.dump(hexes, f, indent=2)

# ---------- RESULT ----------
if previous_owner is None:
    print(f"🌟 Hex {hex_id} CAPTURED!")
else:
    print(f"⚔️ Hex {hex_id} RE-CAPTURED!")

print("New owner:", hex_tile["owner"])
print("New difficulty:", hex_tile["difficulty"])
