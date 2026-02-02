# 🌌 Codelaxy

Codelaxy is a **coding challenge platform prototype** that combines a **Python CLI tool** with a **web-based hexagon map**.  
Players solve programming problems locally, run automated tests, submit their solutions, and **capture hexagons on a shared map** when their solution passes.

The project blends **competitive programming**, **game mechanics**, and **Git-based synchronization** — without requiring a backend server.

---

## 🧠 Core Idea

- Solve coding problems → gain territory  
- Harder problems → stronger control  
- Git acts as the synchronization layer  
- The website visualizes the global game state  

Think: **competitive programming + territory control**.

---

## 🧭 How It Works

1. You **clone the repository**
2. You launch the **Python CLI tool**
   - The CLI automatically runs `git pull` to sync the latest hexagon ownership data
3. You solve a programming problem locally
4. You run automated tests
5. You submit your solution
6. If all tests pass:
   - Hexagon ownership data is updated
   - The CLI **automatically commits** the change back to the repository
7. The website displays the updated hexagon map

---

## 🔺 Hexagon Capture Rules

### 🟪 Unowned Hexagon
- Can be captured by solving a **base difficulty** problem
- If all tests pass:
  - The hexagon becomes owned by the submitter
  - The difficulty level is stored as the hexagon’s strength

### ⚔️ Already Owned Hexagon
- To capture an owned hexagon, you must:
  - Solve a problem with a **higher difficulty level** than the one originally used
- If the submission passes:
  - Ownership is transferred
  - Hexagon data is updated and committed automatically

---

## 🧠 Strategy & Difficulty System

Each hexagon stores the **difficulty level** of the solution that captured it.

- Higher difficulty solutions provide stronger ownership
- Other players must outperform the original solution to take control
- Players must choose between:
  - Capturing many hexagons quickly (lower difficulty)
  - Defending fewer hexagons with harder problems

This introduces **strategic decision-making** alongside algorithmic skill.

---

## ⚙️ Key Features

- 🐍 Python CLI tool for solving, testing, and submitting problems
- 🔄 Automatic `git pull` on CLI launch
- ✅ Local automated test validation
- 🧠 Git-based synchronization (no backend server)
- 🟪 Hexagon-based territory control
- ⚔️ Difficulty-based hexagon stealing mechanics
- 🌐 Web UI for visualizing global ownership
- 📊 JSON-driven map and game state

---

## 🧩 Tech Stack

- **Python** — CLI tool, testing framework, Git automation
- **HTML** — website structure
- **CSS** — layout and visuals
- **JavaScript** — hexagon map rendering and interaction
- **JSON** — hexagon ownership and difficulty data
- **Git** — distributed state synchronization

---



### 1. Clone the repository
```bash
git clone https://github.com/miho2007/codelaxy.git
cd codelaxy


