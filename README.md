# 🚀 **Millennium Falcon Survival Odds Calculator**  

This project calculates the probability of the **Millennium Falcon** successfully reaching its destination while evading the **Empire's fleet**. It provides both a **CLI tool** and a **web application** for users to determine their survival odds.


Test : https://github.com/lioncowlionant/developer-test

---

## ⚡ **Proposed Algorithm** 
DFS(source planet) (O(n^n)) if planet is destination add the current sequence of path from source to destination as a valid path for each planet in neighbour(source planet) mark planet as visited and dont visit it again (also if no fuel is left add a stay on the planet enroute) DFS(planet) backtrack by unmarking the planet

source planet -> The planet where the falcon starts the journey DFS(source planet) -> Generate all valid paths (along with refuelling stay) from source to destianation for each path O(p*n) avoid bounty hunters -> by staying at the previous planet (until the countdown permits one additional day of stay) Finally, find the success percentage corresponding to the minimum number of encounters in any path.

---

## 📦 **Installation**  

To install the required dependencies and set up the package, run the following commands:  

```bash
pip install -r requirements.txt
pip install -e .
```

---

## ⚡ **Command-Line Interface (CLI) Usage**  

Once installed, the CLI can be used with the following command:  

```bash
give-me-the-odds <path_to_millennium-falcon.json> <path_to_empire.json>
```

### ✅ **Example Usage:**  
```bash
give-me-the-odds millenium_falcon/tests/examples/example3/millennium-falcon.json millenium_falcon/tests/examples/example3/empire.json
```

---

## 🌐 **Running the Web App**  

To launch the web application, use the following command:  

```bash
python millenium_falcon/api.py
```

Once the app is running, you can access it at:  
🔗 **[http://localhost:5001/](http://localhost:5001/)**  

### 📂 **Input Files:**  

By default, the **Falcon Inputs** will be taken from the `/inputs` folder in the package root. The following files are required in this folder:  

- `millennium-falcon.json`  
- `universe.db`  

The `empire.json` file should be uploaded via the **frontend**, and the corresponding **success probability** will be displayed on the screen.  

---

## 📜 **Project Overview**  

This tool helps determine the **survival odds** of the **Millennium Falcon** against the Empire's pursuit. Using **graph traversal algorithms** and **probabilistic calculations**, it evaluates the best possible escape routes based on input data.

---

## 🛠 **Technologies Used**  

- **Python** 🐍  
- **Flask** 🌍 (for the web app)  
- **SQLAlchemy** 🗄️ (for database management)  
- **Graph Algorithms** 📊  
- **JSON Parsing** 📜  

---
