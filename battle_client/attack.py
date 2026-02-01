import json
import subprocess
import sys
import os
import random

HEXES_FILE = "../hexes.json"
SESSION_FILE = "session.json"

DIFFICULTY_ORDER = ["easy", "medium", "hard"]


# ---------- GIT HELPER ----------
def run_git(cmd, fail_msg):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(fail_msg)
        print(result.stderr)
        sys.exit(1)


# ---------- LOAD PROBLEM BY DIFFICULTY ----------
def load_problem_for_difficulty(difficulty):
    problems_dir = f"problems/{difficulty}"
    tests_dir = f"tests/{difficulty}"

    if not os.path.isdir(problems_dir):
        print(f"❌ No problems directory for difficulty '{difficulty}'")
        sys.exit(1)

    problem_files = [f for f in os.listdir(problems_dir) if f.endswith(".json")]

    if not problem_files:
        print(f"❌ No problems found for difficulty '{difficulty}'")
        sys.exit(1)

    problem_file = random.choice(problem_files)
    problem_id = problem_file.replace(".json", "")

    with open(f"{problems_dir}/{problem_file}", "r") as f:
        problem = json.load(f)

    test_file = f"{tests_dir}/{problem_id}_test.json"
    if not os.path.exists(test_file):
        print(f"❌ Test file missing: {test_file}")
        sys.exit(1)

    with open(test_file, "r") as f:
        test = json.load(f)

    return problem_id, problem, test


# ---------- SYNC ----------
print("🔄 Syncing galaxy state...")
run_git(["git", "pull"], "❌ Git pull failed. Fix repo state and try again.")


# ---------- LOGIN ----------
print("\n🌌 Galaxy Battle Client")
print("-----------------------")

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


# ---------- LOAD HEXES ----------
with open(HEXES_FILE, "r") as f:
    hexes = json.load(f)

print("\n🗺️ Galaxy Map:")
for h in hexes:
    owner = h["owner"] if h["owner"] else "neutral"
    print(f"  Hex {h['id']} | owner: {owner} | difficulty: {h['difficulty']}")


# ---------- CHOOSE HEX ----------
try:
    hex_id = int(input("\nEnter Hex ID to attack: "))
except ValueError:
    print("❌ Hex ID must be a number")
    sys.exit(1)

hex_tile = next((h for h in hexes if h["id"] == hex_id), None)

if not hex_tile:
    print("❌ Hex not found")
    sys.exit(1)

if hex_tile["owner"] == session["team"]:
    print("❌ You already own this hex.")
    sys.exit(1)

previous_owner = hex_tile["owner"]
difficulty = hex_tile["difficulty"]

print(f"\n⚔️ Attacking Hex {hex_id}")
print("Owner:", previous_owner)
print("Difficulty:", difficulty)


# ---------- LOAD PROBLEM ----------
problem_id, problem, test = load_problem_for_difficulty(difficulty)

print("\n📜 Problem:", problem["title"])
print("Difficulty:", difficulty)
print(problem["description"])
input("\nPress ENTER when ready to run tests...")


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


# ---------- RELOAD HEXES (RACE CHECK) ----------
with open(HEXES_FILE, "r") as f:
    fresh_hexes = json.load(f)

fresh_hex = next(h for h in fresh_hexes if h["id"] == hex_id)

if fresh_hex["owner"] != previous_owner:
    print("⚠️ Hex state changed during attack. Try again.")
    sys.exit(1)


# ---------- CAPTURE ----------
hex_tile["owner"] = session["team"]

if difficulty in DIFFICULTY_ORDER:
    idx = DIFFICULTY_ORDER.index(difficulty)
    if idx < len(DIFFICULTY_ORDER) - 1:
        hex_tile["difficulty"] = DIFFICULTY_ORDER[idx + 1]


# ---------- SAVE ----------
with open(HEXES_FILE, "w") as f:
    json.dump(hexes, f, indent=2)


# ---------- COMMIT + PUSH ----------
commit_msg = (
    f"Capture hex {hex_id} by {session['username']} "
    f"({session['team']}) [{difficulty}->{hex_tile['difficulty']}] "
    f"problem:{problem_id}"
)

print("\n📦 Publishing conquest...")
run_git(["git", "add", HEXES_FILE], "❌ Git add failed")
run_git(["git", "commit", "-m", commit_msg], "❌ Git commit failed")
run_git(["git", "push"], "❌ Git push failed")

print("🚀 Capture complete!")
print("New owner:", hex_tile["owner"])
print("New difficulty:", hex_tile["difficulty"])
